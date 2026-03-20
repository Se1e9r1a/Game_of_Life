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
        self.min_cell_size = 5
        self.max_cell_size = 80

        self.drawing = False
        self.draw_value = 1  # 1 = включаем, 0 = выключаем
        self.panning = False
        self.last_mouse_pos = None

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("white"))
        pen = QPen(QColor("gray"))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)

        if self.cell_size >= 8:
            start_col = int(-self.offset_x // self.cell_size) - 1
            end_col = int((self.width() - self.offset_x) // self.cell_size) + 2
            start_row = int(-self.offset_y // self.cell_size) - 1
            end_row = int((self.height() - self.offset_y) // self.cell_size) + 2

            # вертикальные линии
            for col in range(start_col, end_col):
                x = round(col * self.cell_size + self.offset_x)
                painter.drawLine(x, 0, x, self.height())

            # горизонтальные линии
            for row in range(start_row, end_row):
                y = round(row * self.cell_size + self.offset_y)
                painter.drawLine(0, y, self.width(), y)

        # границы видимой области
        start_col = int((-self.offset_x) // self.cell_size)
        end_col = int((self.width() - self.offset_x) // self.cell_size) + 1
        start_row = int((-self.offset_y) // self.cell_size)
        end_row = int((self.height() - self.offset_y) // self.cell_size) + 1

        # Рисуем только живые клетки
        for (row, col) in self.grid.alive:
            if start_row <= row <= end_row and start_col <= col <= end_col:
                x = int(col * self.cell_size + self.offset_x)
                y = int(row * self.cell_size + self.offset_y)
                painter.fillRect(
                    x,
                    y,
                    self.cell_size,
                    self.cell_size,
                    QColor("green")
                )
                painter.drawRect(
                    x,
                    y,
                    self.cell_size,
                    self.cell_size
                )

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
            if (row, col) in self.grid.alive:
                self.draw_value = 0
            else:
                self.draw_value = 1

            self.grid.toggle_cell(row, col)
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
            current = (row, col) in self.grid.alive

            if self.draw_value == 1 and not current:
                self.grid.alive.add((row, col))

            elif self.draw_value == 0 and current:
                self.grid.alive.remove((row, col))

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

    def wheelEvent(self, event):
        mouse_pos = event.position()
        old_size = self.cell_size

        if event.angleDelta().y() > 0:
            new_size = min(self.cell_size + 2, self.max_cell_size) # ограничение максимального размера
        else:
            new_size = max(self.cell_size - 2, self.min_cell_size) # ограничение минимального размера
        if new_size == old_size:
            return
        scale = new_size / old_size

        # корректируем offset чтобы зум был относительно курсора
        self.offset_x = mouse_pos.x() - scale * (mouse_pos.x() - self.offset_x)
        self.offset_y = mouse_pos.y() - scale * (mouse_pos.y() - self.offset_y)
        self.cell_size = new_size
        self.update()