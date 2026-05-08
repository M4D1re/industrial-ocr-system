from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPainter
from PySide6.QtWidgets import QWidget


class VideoWidget(QWidget):
    """
    Live video display widget.
    """

    def __init__(self) -> None:
        super().__init__()

        self.current_frame: QImage | None = None

        self.setMinimumSize(800, 600)

    def update_frame(self, image: QImage) -> None:
        """
        Updates displayed frame.
        """

        self.current_frame = image

        self.update()

    def paintEvent(self, event) -> None:
        """
        Renders video frame.
        """

        painter = QPainter(self)

        painter.fillRect(self.rect(), Qt.black)

        if self.current_frame:
            scaled = self.current_frame.scaled(
                self.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )

            x = (self.width() - scaled.width()) // 2

            y = (self.height() - scaled.height()) // 2

            painter.drawImage(x, y, scaled)

        else:
            painter.setPen(Qt.white)

            painter.drawText(
                self.rect(),
                Qt.AlignCenter,
                "NO VIDEO SIGNAL",
            )