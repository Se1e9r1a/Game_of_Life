import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from grid import Grid
from styles import main_style
from view import GridView
from ui_controls import ControlPanelTop, ControlPanelLeft
from controller import MainController
from ui_controls import ControlPanelTop, ControlPanelLeft, setup_window

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(main_style)
        self.resize(800, 600)

        self.grid = Grid()
        self.view = GridView(self.grid)
        self.setCentralWidget(self.view)

        self.top_panel = ControlPanelTop()  # панель кнопок управления
        self.left_panel = ControlPanelLeft()  # панель паттернов

        setup_window(self, self.top_panel, self.left_panel)
        self.controller = MainController(self, self.grid, self.view, self.top_panel, self.left_panel)

    def keyPressEvent(self, event):
        self.controller.handle_key_press(event)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())