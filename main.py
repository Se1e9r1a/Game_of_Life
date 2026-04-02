import sys, os
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QStackedWidget, QWidget, QVBoxLayout
from PyQt6.QtCore import QTimer, QUrl, Qt
from grid import Grid
from view import GridView
from ui_controls import setup_window, setup_status_bar, ControlPanelTop, ControlPanelLeft
from controller import MainController
from launcher import StartWindow
from PyQt6.QtGui import QIcon
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from styles import mute_button_style

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game of Life")
        self.resize(800, 600)

        self.setWindowIcon(QIcon("assets/icon.ico"))

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

        self.launcher.theme_combo.currentTextChanged.connect(self.view.apply_theme)

        self.bg_timer = QTimer()
        self.bg_timer.timeout.connect(self.update_bg)
        self.bg_timer.start(100)

        self.stack.addWidget(self.menu_page)

        self.audio_output = QAudioOutput()
        self.music_player = QMediaPlayer()
        self.music_player.setAudioOutput(self.audio_output)
        self.audio_output.setMuted(False)
        
        music_file = get_path("assets/musik.mp3")
        
        self.music_player.setSource(QUrl.fromLocalFile(music_file))
        self.audio_output.setVolume(0.5)
        self.music_player.setLoops(QMediaPlayer.Loops.Infinite)
        self.music_player.play()

        self.btn_mute = QPushButton("🔊", self)
        self.btn_mute.setFixedSize(40, 40)
        self.btn_mute.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_mute.setStyleSheet(mute_button_style)
        self.btn_mute.clicked.connect(self.toggle_mute)
        self.btn_mute.raise_()

        self.statusBar().hide()

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
            self.top_panel.btn_exit.clicked.connect(self.return_to_menu)

            if hasattr(self.top_panel, 'btn_exit'):
                self.top_panel.btn_exit.clicked.connect(self.return_to_menu)
        else:
            self.controller.timer.start()
            self.top_panel.parent().show()
            self.left_panel.parent().show()

        self.controller.update_status_ui()
        self.statusBar().show()

        self.launcher.hide()
        self.view.setFocus()

    def return_to_menu(self):
        if hasattr(self, 'controller'):
            self.controller.timer.stop()
            self.controller.generation = 0
        
        for _ in range(500):
            self.grid.alive.add((random.randint(0, 50), random.randint(0, 70)))
        self.view.reset_view()
        
        self.statusBar().hide()
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

    def resizeEvent(self, event):
        self.btn_mute.move(self.width() - 60, self.height() - 60)
        self.launcher.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def toggle_mute(self):
        is_muted = not self.audio_output.isMuted()
        self.audio_output.setMuted(is_muted)
        self.btn_mute.setText("🔈" if is_muted else "🔊")

    
def get_path(path):
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(bundle_dir, path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())