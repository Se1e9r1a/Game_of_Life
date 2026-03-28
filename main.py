import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout
from PyQt6.QtCore import QTimer
from grid import Grid
from view import GridView
from ui_controls import setup_window, setup_status_bar, ControlPanelTop, ControlPanelLeft
from controller import MainController
from launcher import StartWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game of Life")
        self.resize(800, 600)

        self.grid = Grid()
        self.view = GridView(self.grid)

        for _ in range(500):
            self.grid.alive.add((random.randint(0, 50), random.randint(0, 70)))

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.menu_page = QWidget()
        self.menu_layout = QVBoxLayout(self.menu_page)
        self.menu_layout.setContentsMargins(0, 0, 0, 0)
        self.menu_layout.addWidget(self.view)

        self.launcher = StartWindow(self.menu_page)
        self.launcher.start_game_signal.connect(self.start_game)
        
        self.launcher.setGeometry(0, 0, 800, 600)

        self.bg_timer = QTimer()
        self.bg_timer.timeout.connect(self.update_bg)
        self.bg_timer.start(100)

        self.stack.addWidget(self.menu_page)

    def update_bg(self):
        self.grid.next_generation()
        self.view.update()

    def start_game(self, theme_name):
        self.bg_timer.stop()
        self.view.apply_theme(theme_name)
        self.grid.alive.clear() 

        if not hasattr(self, 'controller'):
            self.top_panel = ControlPanelTop()
            self.left_panel = ControlPanelLeft()
            setup_status_bar(self)
            setup_window(self, self.top_panel, self.left_panel)
            self.controller = MainController(self, self.grid, self.view, self.top_panel, self.left_panel)
            
            if hasattr(self.top_panel, 'btn_exit'):
                self.top_panel.btn_exit.clicked.connect(self.return_to_menu)
        else:
            self.top_panel.parent().show()
            self.left_panel.parent().show()
        
        self.launcher.hide()
        self.view.setFocus()

    def return_to_menu(self):
        self.grid.alive.clear() 
        for _ in range(500):
            self.grid.alive.add((random.randint(0, 50), random.randint(0, 70)))
            
        self.launcher.show()
        self.stack.setCurrentIndex(0)
        self.bg_timer.start(100)
        
        if hasattr(self, 'top_panel'):
            self.top_panel.parent().hide()
        if hasattr(self, 'left_panel'):
            self.left_panel.parent().hide()

    def resizeEvent(self, event):
        self.launcher.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def keyPressEvent(self, event):
        if hasattr(self, 'controller'):
            self.controller.handle_key_press(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())