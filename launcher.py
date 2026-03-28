from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox
from PyQt6.QtCore import Qt, pyqtSignal
from styles import button_style, menu_card_style, theme_combo_style, info_label_style

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

        layout.addWidget(menu_card, alignment=Qt.AlignmentFlag.AlignCenter)