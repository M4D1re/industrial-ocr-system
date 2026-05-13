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
        Adds colored message to logs panel.
        """

        timestamp = datetime.now().strftime("%H:%M:%S")

        colors = {
            "INFO": "#cbd5e1",
            "SUCCESS": "#22c55e",
            "WARNING": "#facc15",
            "ERROR": "#ef4444",
        }

        color = colors.get(level.upper(), "#cbd5e1")

        self.logs.append(
            (
                f"<span style='color:#64748b;'>[{timestamp}]</span> "
                f"<span style='color:{color}; font-weight:600;'>"
                f"[{level.upper()}]</span> "
                f"<span style='color:{color};'>{message}</span>"
            )
        )

    def clear(self) -> None:
        """
        Clears logs panel.
        """

        self.logs.clear()