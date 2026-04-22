from PyQt6.QtCore import Qt
from patterns import PATTERNS
from styles import button_style, pattern_label_style, scroll_bar_style
from PyQt6.QtWidgets import QLineEdit, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QScrollArea
from PyQt6.QtWidgets import QDockWidget
from PyQt6.QtGui import QIntValidator
from styles import button_style, pattern_label_style, scroll_bar_style, exit_button_style

class ControlPanelTop(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(button_style)
        self.main_layout = QHBoxLayout(self)

        self.btn_pause = QPushButton("Пауза")
        self.btn_pause.setCheckable(True)
        self.btn_clear = QPushButton("Очистить")
        self.btn_step = QPushButton("Шаг")
        self.btn_slower = QPushButton("-")
        self.btn_faster = QPushButton("+")

        self.rule_b = QLineEdit("3")
        self.rule_s = QLineEdit("23")
        self.rule_b.setFixedWidth(100)
        self.rule_s.setFixedWidth(100)
        
        numeric_validator = QIntValidator()
        self.rule_b.setValidator(numeric_validator)
        self.rule_s.setValidator(numeric_validator)
        self.rule_b.setMaxLength(8)
        self.rule_s.setMaxLength(8)

        self.main_layout.addStretch()
        
        self.main_layout.addWidget(QLabel("B:"))
        self.main_layout.addWidget(self.rule_b)
        self.main_layout.addWidget(QLabel("S:"))
        self.main_layout.addWidget(self.rule_s)

        self.main_layout.addWidget(self.btn_pause)
        self.main_layout.addWidget(self.btn_clear)
        self.main_layout.addWidget(self.btn_step)
        self.main_layout.addWidget(self.btn_slower)
        self.main_layout.addWidget(self.btn_faster)

        self.main_layout.addStretch()
        self.main_layout.addSpacing(20)

        self.btn_exit = QPushButton("В МЕНЮ")
        self.btn_exit.setStyleSheet(exit_button_style)
        self.main_layout.addWidget(self.btn_exit)

class DraggableLabel(QLabel):
    def __init__(self, pattern_name, parent=None):
        super().__init__(parent)
        self.pattern_name = pattern_name
        self.setText(pattern_name)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(120, 32)
        self.setStyleSheet(pattern_label_style)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            main_win = self.window()
            if hasattr(main_win, 'view'):
                if hasattr(main_win, 'left_panel') and main_win.left_panel.pause_callback:
                    main_win.left_panel.pause_callback()

                main_win.view.start_placement(self.pattern_name, event.globalPosition())


class ControlPanelLeft(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet(scroll_bar_style)

        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setSpacing(8)
        self.container_layout.setContentsMargins(10, 10, 10, 10)
        self.container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.pause_callback = None

        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        for name in PATTERNS:
            label = DraggableLabel(name, self)
            self.container_layout.addWidget(label)

        self.scroll.setWidget(self.container)
        self.main_layout.addWidget(self.scroll)

def setup_window(main_window, top_panel, left_panel):
    # Настройка верхней панели
    dock_top = QDockWidget("Управление", main_window)
    dock_top.setWidget(top_panel)
    dock_top.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
    main_window.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, dock_top)

    # Настройка левой панели
    dock_left = QDockWidget("Паттерны", main_window)
    dock_left.setWidget(left_panel)
    left_panel.setMinimumWidth(150)
    dock_left.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
    main_window.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock_left)
 
def setup_status_bar(window):
    window.label_gen = QLabel("Поколение: 0")
    window.label_zoom = QLabel("Зум: 100%")
    window.label_speed = QLabel("Скорость: 200ms")

    status_style = "margin-right: 15px; color: #cccccc; font-family: Consolas, monospace;"
    window.label_gen.setStyleSheet(status_style)
    window.label_zoom.setStyleSheet(status_style)
    window.label_speed.setStyleSheet(status_style)

    sb = window.statusBar()
    sb.addPermanentWidget(window.label_gen)
    sb.addPermanentWidget(window.label_zoom)
    sb.addPermanentWidget(window.label_speed)