from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtGui import QPen
from patterns import PATTERNS
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt


class GridView(QWidget):
    def __init__(self, grid,parent = None):
        super().__init__(parent)
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

        self.setMouseTracking(True)

        self.is_placing = False  # заменили is_dragging на логичное имя
        self.preview_pattern_coords = None
        self.preview_coords = (0, 0)

        self.theme_colors = {
            "alive": QColor("green"),
            "grid": QColor("gray"),
            "bg": QColor("white")
        }

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.theme_colors["bg"])
        pen = QPen(self.theme_colors["grid"])
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
                
                # Используем цвет живой клетки из темы
                painter.fillRect(
                    x, y, self.cell_size, self.cell_size, 
                    self.theme_colors["alive"]
                )
                painter.drawRect(x, y, self.cell_size, self.cell_size)

        if self.is_placing and self.preview_coords and self.preview_pattern_coords:
            r_origin, c_origin = self.preview_coords
            painter.setBrush(QColor(0, 120, 215, 100))  # Полупрозрачный синий
            painter.setPen(QPen(QColor(0, 120, 215), 1))

            for r, c in self.preview_pattern_coords:
                x = (c + c_origin) * self.cell_size + self.offset_x
                y = (r + r_origin) * self.cell_size + self.offset_y
                painter.drawRect(int(x), int(y), int(self.cell_size), int(self.cell_size))

    def get_cell_from_mouse(self, pos):
        x = pos.x() - self.offset_x
        y = pos.y() - self.offset_y
        col = int(x // self.cell_size)
        row = int(y // self.cell_size)
        return row, col

    def mousePressEvent(self, event):
        if self.is_placing:
            if event.button() == Qt.MouseButton.LeftButton:
                row, col = self.get_cell_from_mouse(event.position())
                for r, c in self.preview_pattern_coords:
                    self.grid.alive.add((r + row, c + col))
                self.is_placing = False
                self.window().controller.toggle_pause()

            elif event.button() == Qt.MouseButton.RightButton:
                self.is_placing = False
                self.window().controller.toggle_pause()

            self.update()
            return

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
        if self.is_placing:
            self.preview_coords = self.get_cell_from_mouse(event.position())
            self.update()
            return

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
            self.offset_x += delta.x()
            self.offset_y += delta.y()

            self.last_mouse_pos = event.position()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False

        elif event.button() == Qt.MouseButton.RightButton:
            self.panning = False


    def wheelEvent(self, event):
        if self.is_placing:
            self.rotate_preview(event.angleDelta().y())
            return

        mouse_pos = event.position()
        old_size = self.cell_size

        if event.angleDelta().y() > 0:
            new_size = min(self.cell_size + 2, self.max_cell_size)
        else:
            new_size = max(self.cell_size - 2, self.min_cell_size)

        if new_size != old_size:
            scale = new_size / old_size
            self.offset_x = mouse_pos.x() - scale * (mouse_pos.x() - self.offset_x)
            self.offset_y = mouse_pos.y() - scale * (mouse_pos.y() - self.offset_y)
            self.cell_size = new_size
            self.update()

    def rotate_preview(self, direction):
        if self.preview_pattern_coords:
            coords = list(self.preview_pattern_coords)
            if direction > 0:
                new_coords = {(c, -r) for r, c in coords}
            else:
                new_coords = {(-c, r) for r, c in coords}

            min_r = min(r for r, c in new_coords)
            min_c = min(c for r, c in new_coords)
            self.preview_pattern_coords = {(r - min_r, c - min_c) for r, c in new_coords}

            self.preview_coords = self.get_cell_from_mouse(self.mapFromGlobal(QCursor.pos()))
            self.update()

    def start_placement(self, pattern_name, global_click_pos=None):
        self.is_placing = True
        self.preview_pattern_coords = set(PATTERNS.get(pattern_name, []))

        if global_click_pos:
            local_pos = self.mapFromGlobal(global_click_pos.toPoint())
            self.preview_coords = self.get_cell_from_mouse(local_pos)
        else:
            self.preview_coords = self.get_cell_from_mouse(self.mapFromGlobal(QCursor.pos()))

        self.setFocus()
        self.update()

    def apply_theme(self, theme_name):
        themes = {
            "Classic Green": {"alive": QColor("#05ca05"), "grid": QColor("#7B7777"), "bg": QColor("#ffffff")},
            "Polar White":   {"alive": QColor("#000000"), "grid": QColor("#cccccc"), "bg": QColor("#ffffff")},
            "Cyberpunk Red": {"alive": QColor("#ff0044"), "grid": QColor("#30000a"), "bg": QColor("#1a0005")}
        }
        self.theme_colors = themes.get(theme_name, themes["Classic Green"])
        self.update()

    def reset_view(self):
        self.cell_size = 20
        self.offset_x = 0
        self.offset_y = 0
        self.update()