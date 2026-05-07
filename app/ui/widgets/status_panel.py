from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)


class StatusPanel(QWidget):
    """
    OCR status panel.
    """

    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(QLabel("OCR Engine Status"))

        self.setLayout(layout)