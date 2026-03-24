import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from grid import Grid
from styles import main_style
from view import GridView
from PyQt6.QtCore import QTimer, Qt
from ui_controls import ControlPanelTop, ControlPanelLeft
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWidgets import QDockWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(main_style)
        self.grid = Grid()
        self.view = GridView(self.grid)
        self.setCentralWidget(self.view)
        self.resize(800, 600)

        self.timer_interval = 200
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_generation)
        self.timer.start(self.timer_interval)

        self.top_panel = ControlPanelTop()  # панель кнопок управления
        self.left_panel = ControlPanelLeft()  # панель паттернов

        # Верхняя панель управления
        dock_top = QDockWidget("Controls", self)
        dock_top.setWidget(self.top_panel)
        dock_top.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, dock_top)

        # запретить открепление
        # dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        # добавить слева
        # self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)

        self.top_panel.btn_pause.clicked.connect(self.toggle_pause)
        self.top_panel.btn_clear.clicked.connect(self.clear)
        self.top_panel.btn_step.clicked.connect(self.step)
        self.top_panel.btn_slower.clicked.connect(self.decrease_speed)
        self.top_panel.btn_faster.clicked.connect(self.increase_speed)

        self.top_panel.btn_pause.clicked.connect(self._return_focus)
        self.top_panel.btn_clear.clicked.connect(self._return_focus)
        self.top_panel.btn_step.clicked.connect(self._return_focus)
        self.top_panel.btn_slower.clicked.connect(self._return_focus)
        self.top_panel.btn_faster.clicked.connect(self._return_focus)

        #QShortcut - то-же самое что и обработка keyPressEvent, только проще
        QShortcut(QKeySequence("Space"), self, self.toggle_pause)
        QShortcut(QKeySequence("="), self, self.increase_speed)
        QShortcut(QKeySequence("-"), self, self.decrease_speed)

        # Левая панель паттернов
        dock_left = QDockWidget("Patterns", self)
        dock_left.setWidget(self.left_panel)
        self.left_panel.setMinimumWidth(150)
        dock_left.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock_left)

        self.left_panel.pause_callback = self.force_pause

    def _return_focus(self):
        self.view.setFocus()
    
    def next_generation(self):
        self.grid.next_generation()
        self.view.update()

    def keyPressEvent(self, event):
        key = event.text().lower()

        # N/Т — один шаг
        if key in ('n','т'):
            self.step()

        # C/С — очистить поле
        elif key in ('c','с'):
            self.clear()

    def force_pause(self):
        if self.timer.isActive():
            self.timer.stop()
            self.top_panel.btn_pause.setChecked(True)

    def toggle_pause(self):
        if self.timer.isActive():
            self.timer.stop()
            self.top_panel.btn_pause.setChecked(True)
        else:
            self.timer.start(self.timer_interval)
            self.top_panel.btn_pause.setChecked(False)

    def clear(self):
        self.grid.alive.clear()
        self.view.update()
        self.top_panel.btn_clear.setDown(True)
        QTimer.singleShot(100, lambda: self.top_panel.btn_clear.setDown(False))

    def step(self):
        self.grid.next_generation()
        self.view.update()
        self.top_panel.btn_step.setDown(True)
        QTimer.singleShot(100, lambda: self.top_panel.btn_step.setDown(False))

    def increase_speed(self):
        self.timer_interval = max(1, self.timer_interval - 20)
        self.timer.setInterval(self.timer_interval)
        self.view.update()

        self.top_panel.btn_faster.setDown(True)
        QTimer.singleShot(100, lambda: self.top_panel.btn_faster.setDown(False))

    def decrease_speed(self):
        self.timer_interval += 20
        self.timer.setInterval(self.timer_interval)

        self.top_panel.btn_slower.setDown(True)
        QTimer.singleShot(100, lambda: self.top_panel.btn_slower.setDown(False))

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())