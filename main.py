import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from grid import Grid
from view import GridView
from PyQt6.QtCore import QTimer, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.grid = Grid()
        self.view = GridView(self.grid)
        self.setCentralWidget(self.view)
        self.resize(800, 600)
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_generation)
        self.timer.start(200)
    
    def next_generation(self):
        self.grid.next_generation()
        self.view.update()

    def keyPressEvent(self, event):
        
        key = event.text().lower()
        
        # Space — старт / пауза
        if event.key() == Qt.Key.Key_Space:
            if self.timer.isActive():
                self.timer.stop()
            else:
                self.timer.start(200)

        # N/Т — один шаг
        elif key in ('n','т'):
            self.grid.next_generation()
            self.view.update()

        # C/С — очистить поле
        elif key in ('c','с'):
            self.grid.alive.clear()
            self.view.update()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())