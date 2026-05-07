from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QWidget


class VideoWidget(QWidget):
    """
    Central video display widget.
    """

    def __init__(self) -> None:
        super().__init__()

        self.setMinimumSize(800, 600)

    def paintEvent(self, event) -> None:
        """
        Paints placeholder video background.
        """

        painter = QPainter(self)

        painter.fillRect(self.rect(), QColor("#1e1e1e"))

        painter.setPen(Qt.white)

        painter.drawText(
            self.rect(),
            Qt.AlignCenter,
            "LIVE VIDEO STREAM",
        )