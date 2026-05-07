from PySide6.QtWidgets import (
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class LogsPanel(QWidget):
    """
    System logs panel.
    """

    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout()

        self.logs = QTextEdit()

        self.logs.setReadOnly(True)

        layout.addWidget(self.logs)

        self.setLayout(layout)