DARK_THEME = """
QWidget {
    background-color: #2b2b2b;
    color: #ffffff;
    font-size: 12px;
    font-family: Segoe UI;
}

QMainWindow {
    background-color: #2b2b2b;
}

QMenuBar {
    background-color: #353535;
}

QStatusBar {
    background-color: #353535;
}

/* TOOLBAR */

QToolBar {
    background-color: #353535;
    border-bottom: 1px solid #444444;
    spacing: 6px;
    padding: 4px;
}

/* BUTTONS */

QPushButton {
    background-color: #3c3f41;
    border: 1px solid #555555;
    border-radius: 6px;
    padding: 6px 12px;
}

QPushButton:hover {
    background-color: #4b4f52;
    border: 1px solid #6a95ff;
}

QPushButton:pressed {
    background-color: #2d5fb8;
    border: 1px solid #82aaff;
    padding-left: 8px;
    padding-top: 8px;
}

/* TOOLBAR BUTTONS */

QToolButton {
    background-color: #3c3f41;
    border: 1px solid #555555;
    border-radius: 6px;
    padding: 6px 12px;
    margin: 2px;
}

QToolButton:hover {
    background-color: #4b4f52;
    border: 1px solid #6a95ff;
}

QToolButton:pressed {
    background-color: #2d5fb8;
    border: 1px solid #82aaff;
    padding-left: 8px;
    padding-top: 8px;
}

/* INPUTS */

QSpinBox {
    background-color: #3c3f41;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 4px;
}

QSpinBox:focus {
    border: 1px solid #6a95ff;
}

/* TABLES */

QTableWidget {
    background-color: #313335;
    gridline-color: #444444;
    border: 1px solid #444444;
}

QHeaderView::section {
    background-color: #3c3f41;
    padding: 4px;
    border: 1px solid #444444;
}

/* LISTS */

QListWidget {
    background-color: #313335;
    border: 1px solid #444444;
}

QListWidget::item:selected {
    background-color: #2d5fb8;
}
"""