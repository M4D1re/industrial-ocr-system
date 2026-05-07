from PySide6.QtWidgets import (
    QLabel,
    QListWidget,
    QVBoxLayout,
    QWidget,
)


class CameraPanel(QWidget):
    """
    Camera management panel.
    """

    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("Connected Cameras")

        self.camera_list = QListWidget()

        layout.addWidget(title)

        layout.addWidget(self.camera_list)

        self.setLayout(layout)