from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QShortcut, QKeySequence

class MainController:
    # Все необходимые элементы из main.py
    def __init__(self, window, grid, view, top_panel, left_panel):
        self.window = window
        self.grid = grid
        self.view = view
        self.top_panel = top_panel
        self.left_panel = left_panel

        self.timer_interval = 200
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_generation)
        self.timer.start(self.timer_interval)

        # Подключаем все кнопки и хоткеи
        self.connect_signals()

    def connect_signals(self):
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

        QShortcut(QKeySequence("Space"), self.window, self.toggle_pause)
        QShortcut(QKeySequence("="), self.window, self.increase_speed)
        QShortcut(QKeySequence("-"), self.window, self.decrease_speed)

        # Передаем функцию force_pause в левую панель
        self.left_panel.pause_callback = self.force_pause

    def handle_key_press(self, event):
        """Эта функция вызывается из main.py при нажатии кнопок"""
        key = event.text().lower()
        if key in ('n', 'т'):
            self.step()
        elif key in ('c', 'с'):
            self.clear()

    def _return_focus(self):
        self.view.setFocus()
    
    def next_generation(self):
        self.grid.next_generation()
        self.view.update()

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
        self.timer_interval = max(1, self.timer_interval - 40)
        self.timer.setInterval(self.timer_interval)
        self.view.update()
        self.top_panel.btn_faster.setDown(True)
        QTimer.singleShot(100, lambda: self.top_panel.btn_faster.setDown(False))

    def decrease_speed(self):
        self.timer_interval += 40
        self.timer.setInterval(self.timer_interval)
        self.top_panel.btn_slower.setDown(True)
        QTimer.singleShot(100, lambda: self.top_panel.btn_slower.setDown(False))