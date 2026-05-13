DARK_THEME = """
QWidget {
    background-color: #20242b;
    color: #e8edf2;
    font-size: 12px;
    font-family: Segoe UI;
}

QMainWindow {
    background-color: #20242b;
}

QMenuBar {
    background-color: #252b33;
    border-bottom: 1px solid #343c46;
}

QStatusBar {
    background-color: #252b33;
    color: #b8c3cf;
    border-top: 1px solid #343c46;
}

/* TOOLBAR */

QToolBar {
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #2f3742,
        stop:1 #252b33
    );
    border-bottom: 1px solid #3d4652;
    spacing: 8px;
    padding: 6px;
}

QToolBar QLabel {
    background: transparent;
    color: #cbd5e1;
    padding-left: 6px;
}

/* TOOLBAR BUTTONS */

QToolButton {
    background-color: #344054;
    color: #f8fafc;
    border: 1px solid #475569;
    border-radius: 8px;
    padding: 7px 13px;
    margin: 2px;
}

QToolButton:hover {
    background-color: #3f4f68;
    border: 1px solid #60a5fa;
}

QToolButton:pressed {
    background-color: #2563eb;
    border: 1px solid #93c5fd;
    padding-left: 10px;
    padding-top: 9px;
}

/* NORMAL BUTTONS */

QPushButton {
    background-color: #344054;
    color: #f8fafc;
    border: 1px solid #475569;
    border-radius: 8px;
    padding: 7px 12px;
}

QPushButton:hover {
    background-color: #3f4f68;
    border: 1px solid #60a5fa;
}

QPushButton:pressed {
    background-color: #2563eb;
    border: 1px solid #93c5fd;
    padding-left: 9px;
    padding-top: 9px;
}

/* INPUTS */

QSpinBox {
    background-color: #111827;
    color: #e5e7eb;
    border: 1px solid #4b5563;
    border-radius: 7px;
    padding-left: 8px;
    padding-right: 22px;
    min-height: 28px;
}

QSpinBox:focus {
    border: 1px solid #60a5fa;
}

QSpinBox::up-button {
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 20px;
    border-left: 1px solid #4b5563;
    border-bottom: 1px solid #4b5563;
    border-top-right-radius: 7px;
    background-color: #374151;
}

QSpinBox::up-button:hover {
    background-color: #2563eb;
}

QSpinBox::down-button {
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 20px;
    border-left: 1px solid #4b5563;
    border-bottom-right-radius: 7px;
    background-color: #374151;
}

QSpinBox::down-button:hover {
    background-color: #2563eb;
}

QSpinBox::up-arrow {
    width: 0px;
    height: 0px;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-bottom: 6px solid #e5e7eb;
}

QSpinBox::down-arrow {
    width: 0px;
    height: 0px;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #e5e7eb;
}

/* DOCKS */

QDockWidget {
    titlebar-close-icon: none;
    titlebar-normal-icon: none;
    color: #e5e7eb;
    font-weight: 600;
}

QDockWidget::title {
    background-color: #2f3742;
    padding: 7px;
    border-bottom: 1px solid #3d4652;
}

/* LISTS */

QListWidget {
    background-color: #111827;
    color: #e5e7eb;
    border: 1px solid #374151;
    border-radius: 8px;
    padding: 4px;
}

QListWidget::item {
    padding: 6px;
    border-radius: 5px;
}

QListWidget::item:hover {
    background-color: #263244;
}

QListWidget::item:selected {
    background-color: #2563eb;
    color: #ffffff;
}

/* TEXT EDIT */

QTextEdit {
    background-color: #0f172a;
    color: #cbd5e1;
    border: 1px solid #374151;
    border-radius: 8px;
    padding: 6px;
}

/* TABLES */

QTableWidget {
    background-color: #111827;
    color: #e5e7eb;
    gridline-color: #374151;
    border: 1px solid #374151;
    border-radius: 8px;
}

QTableWidget::item {
    padding: 5px;
}

QHeaderView::section {
    background-color: #2f3742;
    color: #e5e7eb;
    padding: 6px;
    border: 1px solid #3d4652;
}

/* MESSAGE BOX */

QMessageBox {
    background-color: #20242b;
}

QMessageBox QLabel {
    color: #e5e7eb;
}
"""