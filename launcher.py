from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox
from PyQt6.QtCore import Qt, pyqtSignal
from styles import button_style, menu_card_style, theme_combo_style, info_label_style, help_box_style, help_button_style

class StartWindow(QWidget):
    start_game_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QVBoxLayout(self)
        
        menu_card = QWidget()
        menu_card.setStyleSheet(menu_card_style)
        menu_card.setFixedWidth(420)
        
        card_layout = QVBoxLayout(menu_card)
        card_layout.setSpacing(10)
        card_layout.setContentsMargins(25, 25, 25, 25)
        
        title = QLabel("GAME OF LIFE")
        title.setStyleSheet("color: #00ff00; font-size: 32px; font-weight: bold; font-family: 'Consolas'; background: transparent; margin-bottom: 10px;")
        card_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        rules_label = QLabel("ПРАВИЛА:\n• Клетка оживает, если рядом 3 соседа\n• Клетка выживает, если рядом 2 или 3 соседа\n• В противном случае — клетка погибает")
        rules_label.setStyleSheet(info_label_style)
        card_layout.addWidget(rules_label)

        theme_label = QLabel("Выберите тему:")
        theme_label.setStyleSheet("color: #888; font-size: 12px; margin-top: 10px;")
        card_layout.addWidget(theme_label)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Classic Green", "Cyberpunk Red", "Polar White"])
        self.theme_combo.setStyleSheet(theme_combo_style)
        card_layout.addWidget(self.theme_combo)

        self.btn_start = QPushButton("ИГРАТЬ")
        self.btn_start.setStyleSheet(button_style)
        self.btn_start.setFixedSize(370, 50)
        self.btn_start.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_start.clicked.connect(lambda: self.start_game_signal.emit(self.theme_combo.currentText()))
        card_layout.addWidget(self.btn_start, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.btn_help = QPushButton("?", menu_card)
        self.btn_help.setFixedSize(24, 24)
        self.btn_help.move(385, 10)
        self.btn_help.setStyleSheet(help_button_style)
        self.btn_help.setCursor(Qt.CursorShape.PointingHandCursor)

        self.controls_info = QLabel(
            "<b>УПРАВЛЕНИЕ</b><br><br>"
            "<b>ЛКМ:</b> Рисовать клетки<br>"
            "<b>ПКМ:</b> Перемещать камеру<br>"
            "<b>Колесо:</b> Зум +/-<br>"
            "<b>Space:</b> Пауза/Старт<br>"
            "<b>Колесов:</b> Поворот паттерна в режиме размещения<br>"
            "<b>C:</b> Очистить поле"
        )
        self.controls_info.setStyleSheet(help_box_style)
        self.controls_info.setWordWrap(True)
        self.controls_info.hide()
        
        card_layout.addWidget(self.controls_info)
        
        self.btn_help.clicked.connect(self.toggle_help)

        layout.addWidget(menu_card, alignment=Qt.AlignmentFlag.AlignCenter)
    
    def update_preview_theme(self, theme_name):
        themes = {
            "Classic Green": "#00ff00",
            "Cyberpunk Red": "#ff0044",
            "Polar White": "#ffffff"
        }
        color = themes.get(theme_name, "#00ff00")

        self.title.setStyleSheet(f"color: {color}; font-size: 32px; font-weight: bold; font-family: 'Consolas';")
        self.theme_combo.setStyleSheet(f"background-color: #000; color: {color}; border: 1px solid {color}; border-radius: 4px; padding: 5px;")
        self.btn_start.setStyleSheet(f"background-color: {color}; color: #000; border-radius: 5px; font-weight: bold; font-size: 16px;")
        self.controls_label.setStyleSheet(f"color: #888; font-size: 12px; background: rgba(0, 0, 0, 50); padding: 8px; border-radius: 5px; border-left: 3px solid {color};")

    def toggle_help(self):
        if self.controls_info.isHidden():
            self.controls_info.show()
            self.btn_help.setText("X")
        else:
            self.controls_info.hide()
            self.btn_help.setText("?")