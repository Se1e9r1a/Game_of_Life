from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox
from PyQt6.QtCore import Qt, pyqtSignal
from styles import button_style

class StartWindow(QWidget):
    start_game_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QVBoxLayout(self)
        
        menu_card = QWidget()
        menu_card.setStyleSheet("background-color: rgba(30, 30, 30, 220); border-radius: 15px;")
        menu_card.setFixedSize(320, 280)
        
        card_layout = QVBoxLayout(menu_card)
        card_layout.setSpacing(20)
        card_layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("GAME OF LIFE")
        title.setStyleSheet("color: #00ff00; font-size: 26px; font-weight: bold; font-family: 'Consolas'; background: transparent;")
        card_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Classic Green", "Cyberpunk Red", "Polar White"])
        self.theme_combo.setStyleSheet("""
            QComboBox {
                background-color: #000000;
                color: #00ff00;
                border: 2px solid #00ff00;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
                min-width: 200px;
            }
            QComboBox::drop-down {
                border: 0px;
            }
            QComboBox QAbstractItemView {
                background-color: #1a1a1a;
                color: #00ff00;
                selection-background-color: #00ff00;
                selection-color: #000000;
                outline: 0px;
            }
        """)
        card_layout.addWidget(self.theme_combo, alignment=Qt.AlignmentFlag.AlignCenter)

        self.btn_start = QPushButton("ИГРАТЬ")
        self.btn_start.setStyleSheet(button_style)
        self.btn_start.setFixedSize(200, 50)
        self.btn_start.clicked.connect(lambda: self.start_game_signal.emit(self.theme_combo.currentText()))
        card_layout.addWidget(self.btn_start, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(menu_card, alignment=Qt.AlignmentFlag.AlignCenter)