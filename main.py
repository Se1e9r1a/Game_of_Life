import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from grid import Grid
from view import GridView
from PyQt6.QtCore import QTimer, Qt
from ui_controls import ControlPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.grid = Grid()
        self.view = GridView(self.grid)
        self.setCentralWidget(self.view)
        self.resize(800, 600)

        self.timer_interval = 200
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_generation)
        self.timer.start(self.timer_interval)

        self.control_panel = ControlPanel()
        self.addToolBarBreak()
        self.setMenuWidget(self.control_panel)
        self.control_panel.btn_pause.clicked.connect(self.toggle_pause)
        self.control_panel.btn_step.clicked.connect(self.step)
        self.control_panel.btn_slower.clicked.connect(self.decrease_speed)
        self.control_panel.btn_faster.clicked.connect(self.increase_speed)

        self.control_panel.btn_pause.clicked.connect(self._return_focus)
        self.control_panel.btn_step.clicked.connect(self._return_focus)
        self.control_panel.btn_slower.clicked.connect(self._return_focus)
        self.control_panel.btn_faster.clicked.connect(self._return_focus)

    def _return_focus(self):
        self.view.setFocus()
    
    def next_generation(self):
        self.grid.next_generation()
        self.view.update()

    def keyPressEvent(self, event):
        key = event.text().lower()

        # Space — старт / пауза
        if event.key() == Qt.Key.Key_Space:
            self.toggle_pause()
        # N/Т — один шаг
        elif key in ('n','т'):
            self.step()
            self.view.update()

        # C/С — очистить поле
        elif key in ('c','с'):
            self.grid.alive.clear()
            self.view.update()

        # +/- увеличить/уменьшить скорость генерации
        elif key in ('+', '='):
            self.increase_speed()

        elif key == '-':
            self.decrease_speed()

    def toggle_pause(self):
        if self.timer.isActive():
            self.timer.stop()
            self.control_panel.btn_pause.setChecked(True)
        else:
            self.timer.start(self.timer_interval)
            self.control_panel.btn_pause.setChecked(False)

    def step(self):
        self.grid.next_generation()
        self.view.update()
        self.control_panel.btn_step.setDown(True)
        QTimer.singleShot(100, lambda: self.control_panel.btn_step.setDown(False))

    def increase_speed(self):
        self.timer_interval = max(10, self.timer_interval - 20)
        self.timer.setInterval(self.timer_interval)
        self.grid.next_generation()
        self.view.update()

        self.control_panel.btn_faster.setDown(True)
        QTimer.singleShot(100, lambda: self.control_panel.btn_faster.setDown(False))

    def decrease_speed(self):
        self.timer_interval += 20
        self.timer.setInterval(self.timer_interval)

        self.control_panel.btn_slower.setDown(True)
        QTimer.singleShot(100, lambda: self.control_panel.btn_slower.setDown(False))

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())