from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen

class GridView(QWidget):
    def __init__(self, grid):
        super().__init__()
        self.grid = grid
        self.cell_size = 20
        self.offset_x = 0
        self.offset_y = 0
        self.drawing = False
        self.draw_value = 1  # 1 = включаем, 0 = выключаем
        self.panning = False
        self.last_mouse_pos = None

    def paintEvent(self, event):
        painter = QPainter(self)
        # фон
        painter.fillRect(self.rect(), QColor("white"))

        pen = QPen(QColor("gray"))
        pen.setWidth(1)
        painter.setPen(pen)

        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                x = col * self.cell_size + self.offset_x
                y = row * self.cell_size + self.offset_y
                # живая клетка
                if self.grid.cells[row][col] == 1:
                    painter.fillRect(x, y,
                                     self.cell_size,
                                     self.cell_size,
                                     QColor("green"))
                # сетка
                painter.drawRect(x, y,
                                 self.cell_size,
                                 self.cell_size)

    def get_cell_from_mouse(self, pos):
        x = pos.x() - self.offset_x
        y = pos.y() - self.offset_y
        col = int(x // self.cell_size)
        row = int(y // self.cell_size)
        return row, col

    def mousePressEvent(self, event):
        # Рисование ЛКМ
        if event.button() == Qt.MouseButton.LeftButton:
            row, col = self.get_cell_from_mouse(event.position())
            if 0 <= row < self.grid.rows and 0 <= col < self.grid.cols:
                # Определяем режим рисования
                if self.grid.cells[row][col] == 1:
                    self.draw_value = 0
                else:
                    self.draw_value = 1
                self.grid.cells[row][col] = self.draw_value
                self.drawing = True
                self.update()
        # Перемещение камеры ПКМ
        elif event.button() == Qt.MouseButton.RightButton:
            self.panning = True
            self.last_mouse_pos = event.position()

    def mouseMoveEvent(self, event):
        # Рисование ЛКМ
        if self.drawing:
            row, col = self.get_cell_from_mouse(event.position())

            if 0 <= row < self.grid.rows and 0 <= col < self.grid.cols:
                self.grid.cells[row][col] = self.draw_value
                self.update()

        # Перемещение камеры ПКМ
        if self.panning:
            delta = event.position() - self.last_mouse_pos

            self.offset_x += int(delta.x())
            self.offset_y += int(delta.y())

            self.last_mouse_pos = event.position()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False

        elif event.button() == Qt.MouseButton.RightButton:
            self.panning = False