from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout

class ControlPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.btn_pause = QPushButton("Pause")
        self.btn_pause.setCheckable(True)
        self.btn_step = QPushButton("Step")
        self.btn_slower = QPushButton("-")
        self.btn_faster = QPushButton("+")
        self.layout.addWidget(self.btn_pause)
        self.layout.addWidget(self.btn_step)
        self.layout.addWidget(self.btn_slower)
        self.layout.addWidget(self.btn_faster)