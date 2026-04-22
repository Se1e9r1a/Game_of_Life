from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWidgets import QLabel

class MainController:
    def __init__(self, window, grid, view, top_panel, left_panel):
        self.window = window
        self.grid = grid
        self.view = view
        self.top_panel = top_panel
        self.left_panel = left_panel

        self.generation = 0
        self.timer_interval = 200
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_generation)
        self.timer.start(self.timer_interval)

        self.top_panel.rule_b.textChanged.connect(self.update_rules)
        self.top_panel.rule_s.textChanged.connect(self.update_rules)

        # Подключаем все кнопки и хоткеи
        self.connect_signals()

        self.update_status_ui()

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
        self.generation = self.generation + 1
        self.view.update()
        self.update_status_ui()

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
        self.generation = 0
        self.update_status_ui()

    def step(self):
        self.grid.next_generation()
        self.view.update()
        self.top_panel.btn_step.setDown(True)
        QTimer.singleShot(100, lambda: self.top_panel.btn_step.setDown(False))
        self.generation = self.generation + 1
        self.update_status_ui()

    def increase_speed(self):
        self.timer_interval = max(1, self.timer_interval - 40)
        self.timer.setInterval(self.timer_interval)
        self.view.update()
        self.top_panel.btn_faster.setDown(True)
        QTimer.singleShot(100, lambda: self.top_panel.btn_faster.setDown(False))
        self.update_status_ui()

    def decrease_speed(self):
        self.timer_interval += 40
        self.timer.setInterval(self.timer_interval)
        self.top_panel.btn_slower.setDown(True)
        QTimer.singleShot(100, lambda: self.top_panel.btn_slower.setDown(False))
        self.update_status_ui()

    
    def update_status_ui(self):
        zoom_value = int(self.view.cell_size * 5)
        
        self.window.label_gen.setText("Поколение: " + str(self.generation))
        self.window.label_zoom.setText("Зум: " + str(zoom_value) + "%")
        self.window.label_speed.setText("Скорость: " + str(self.timer_interval) + "ms")

    def update_rules(self):
        # 3 -> 3, 23 -> 2, 3
        b_text = self.top_panel.rule_b.text()
        s_text = self.top_panel.rule_s.text()
        
        try:
            self.grid.birth_rules = [int(d) for d in b_text if d.isdigit()]
            self.grid.survive_rules = [int(d) for d in s_text if d.isdigit()]
        except:
            pass

def setup_status_bar(window):
    window.label_gen = QLabel("Поколение: 0")
    window.label_zoom = QLabel("Зум: 100%")
    window.label_speed = QLabel("Скорость: 200ms")

    window.statusBar().addPermanentWidget(window.label_gen)
    window.statusBar().addPermanentWidget(window.label_zoom)
    window.statusBar().addPermanentWidget(window.label_speed)