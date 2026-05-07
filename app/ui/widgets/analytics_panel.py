from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)


class AnalyticsPanel(QWidget):
    """
    Analytics panel.
    """

    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Analytics Charts"))

        self.setLayout(layout)