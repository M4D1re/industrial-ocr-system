from datetime import datetime

from PySide6.QtWidgets import QTextEdit, QVBoxLayout, QWidget


class LogsPanel(QWidget):
    """
    System logs panel.
    """

    def __init__(self) -> None:
        super().__init__()

        self.logs = QTextEdit()
        self.logs.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.logs)

        self.setLayout(layout)

    def add_log(self, message: str, level: str = "INFO") -> None:
        """
        Adds message to logs panel.
        """

        timestamp = datetime.now().strftime("%H:%M:%S")

        self.logs.append(
            f"[{timestamp}] [{level}] {message}"
        )

    def clear(self) -> None:
        """
        Clears logs panel.
        """

        self.logs.clear()