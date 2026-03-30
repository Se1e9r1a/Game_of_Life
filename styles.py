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

menu_card_style = "background-color: rgba(30, 30, 30, 230); border: 1px solid #444; border-radius: 15px;"

theme_combo_style = """
    QComboBox { 
        background-color: #000; color: #00ff00; border: 1px solid #00ff00; 
        border-radius: 4px; padding: 5px; font-weight: bold; 
    }
    QComboBox QAbstractItemView { background-color: #1a1a1a; color: #00ff00; }
"""

info_label_style = "color: #bbb; font-size: 13px; background: rgba(255, 255, 255, 10); padding: 10px; border-radius: 5px;"

controls_label_style = """
    color: #888; font-size: 12px; background: rgba(0, 0, 0, 50); 
    padding: 8px; border-radius: 5px; border-left: 3px solid #00ff00;
"""

exit_button_style = """
    QPushButton {
        background-color: #444; 
        color: white; 
        border-radius: 5px; 
        padding: 5px 15px; 
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #666;
    }
"""

help_box_style = """
    QLabel {
        background-color: rgba(20, 20, 20, 240);
        color: #aaa;
        border: 1px solid #444;
        border-radius: 8px;
        padding: 15px;
        font-size: 12px;
    }
"""

help_button_style = """
    QPushButton {
        background-color: transparent;
        color: #555;
        font-size: 18px;
        font-weight: bold;
        border: 1px solid #444;
        border-radius: 12px;
    }
    QPushButton:hover {
        color: #00ff00;
        border-color: #00ff00;
    }
"""