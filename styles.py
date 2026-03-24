main_style = """
    QMainWindow {
        background-color: #1e1e1e;
    }
    QDockWidget {
        color: white;
        font-weight: bold;
    }
    QDockWidget::title {
        background-color: #252526;
        padding-top: 4px;
        padding-left: 10px;
    }
"""

button_style = """
    QPushButton {
        background-color: #333333;
        color: white;
        border: 1px solid #444444;
        border-radius: 4px;
        padding: 5px 15px;
        font-weight: bold;
        min-width: 60px;
    }
    QPushButton:hover {
        background-color: #444444;
    }
    QPushButton:pressed {
        background-color: #222222;
    }
    QPushButton:checked {
        background-color: #d32f2f;
    }
"""

pattern_label_style = """
    QLabel {
        background-color: #252526;
        color: #d4d4d4;            
        border: 1px solid #333333;
        border-radius: 6px;
        font-size: 12px;
        font-family: "Segoe UI", sans-serif;
        padding-left: 5px;
    }
    
    QLabel:hover {
        background-color: #2a2d2e;
        color: #569cd6;
        border: 1px solid #007acc;
    }
"""

scroll_bar_style = """
    QScrollArea {
        border: none;
        background-color: transparent;
    }
    QScrollBar:vertical {
        border: none;
        background: #252526;
        width: 10px;
        margin: 0px 0px 0px 0px;
    }
    QScrollBar::handle:vertical {
        background: #3e3e42;
        min-height: 20px;
        border-radius: 5px;
    }
    QScrollBar::handle:vertical:hover {
        background: #505050;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
"""