import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from grid import Grid
from view import GridView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.grid = Grid(50, 50)
        self.view = GridView(self.grid)
        self.setCentralWidget(self.view)
        self.resize(800, 600)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())