import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSlider, QSpinBox, QComboBox, QCheckBox,
    QRadioButton, QProgressBar, QTextEdit, QDockWidget,
    QMessageBox, QToolBar
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Demo GUI Application - PyQt6")
        self.setMinimumSize(900, 600)

        # ================= MENU =================
        menu = self.menuBar()

        file_menu = menu.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menu.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        # ================= TOOLBAR =================
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        start_action = QAction("Start", self)
        start_action.triggered.connect(self.start_progress)
        toolbar.addAction(start_action)

        stop_action = QAction("Stop", self)
        stop_action.triggered.connect(self.stop_progress)
        toolbar.addAction(stop_action)

        # ================= STATUS BAR =================
        self.statusBar().showMessage("Ready")

        # ================= CENTRAL WIDGET =================
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # ===== Left Panel =====
        left_layout = QVBoxLayout()

        self.label = QLabel("Speed:")
        left_layout.addWidget(self.label)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(1, 100)
        self.slider.valueChanged.connect(self.slider_changed)
        left_layout.addWidget(self.slider)

        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, 100)
        self.spinbox.valueChanged.connect(self.spinbox_changed)
        left_layout.addWidget(self.spinbox)

        self.combo = QComboBox()
        self.combo.addItems(["Option 1", "Option 2", "Option 3"])
        left_layout.addWidget(self.combo)

        self.checkbox = QCheckBox("Enable feature")
        left_layout.addWidget(self.checkbox)

        self.radio1 = QRadioButton("Mode A")
        self.radio2 = QRadioButton("Mode B")
        left_layout.addWidget(self.radio1)
        left_layout.addWidget(self.radio2)

        self.button = QPushButton("Show Message")
        self.button.clicked.connect(self.show_message)
        left_layout.addWidget(self.button)

        self.progress = QProgressBar()
        left_layout.addWidget(self.progress)

        main_layout.addLayout(left_layout)

        # ===== Right Panel =====
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Log output...")
        main_layout.addWidget(self.text_edit)

        # ================= DOCK WIDGET =================
        dock = QDockWidget("Additional Panel", self)
        dock_label = QLabel("Dockable content here")
        dock.setWidget(dock_label)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

        # ================= TIMER =================
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.progress_value = 0

    # ================= METHODS =================

    def slider_changed(self, value):
        self.spinbox.setValue(value)
        self.statusBar().showMessage(f"Slider: {value}")

    def spinbox_changed(self, value):
        self.slider.setValue(value)

    def show_message(self):
        QMessageBox.information(self, "Information", "Button clicked!")
        self.text_edit.append("Button was clicked.")

    def show_about(self):
        QMessageBox.about(self, "About", "Demo GUI built with PyQt6")

    def start_progress(self):
        self.progress_value = 0
        self.timer.start(50)
        self.statusBar().showMessage("Progress started")

    def stop_progress(self):
        self.timer.stop()
        self.statusBar().showMessage("Progress stopped")

    def update_progress(self):
        self.progress_value += 1
        self.progress.setValue(self.progress_value)
        if self.progress_value >= 100:
            self.timer.stop()
            self.statusBar().showMessage("Completed!")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())