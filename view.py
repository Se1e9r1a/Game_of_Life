from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt

class GridView(QWidget):
    def __init__(self, grid):
        super().__init__()
        self.grid = grid
        self.cell_size = 20
        self.offset_x = 0
        self.offset_y = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("white"))

        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                x = col * self.cell_size + self.offset_x
                y = row * self.cell_size + self.offset_y

                if self.grid.cells[row][col] == 1:
                    painter.setBrush(QColor("green"))
                    painter.fillRect(x, y, self.cell_size, self.cell_size)
                    painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.drawRect(x,y,self.cell_size,self.cell_size)