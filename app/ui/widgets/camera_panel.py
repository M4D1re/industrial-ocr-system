from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QLabel,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.models.camera_model import CameraModel


class CameraPanel(QWidget):
    """
    Camera management panel.
    """

    add_camera_requested = Signal()

    camera_selected = Signal(object)

    def __init__(self) -> None:
        super().__init__()

        self.cameras: dict[int, CameraModel] = {}

        layout = QVBoxLayout()

        title = QLabel("Connected Cameras")

        self.camera_list = QListWidget()

        self.camera_list.itemClicked.connect(
            self._on_camera_clicked
        )

        self.add_camera_button = QPushButton("Add Camera")

        self.add_camera_button.clicked.connect(
            self.add_camera_requested.emit
        )

        layout.addWidget(title)

        layout.addWidget(self.camera_list)

        layout.addWidget(self.add_camera_button)

        self.setLayout(layout)

    def set_cameras(self, cameras: list[CameraModel]) -> None:
        """
        Displays cameras in list.
        """

        self.cameras.clear()

        self.camera_list.clear()

        for camera in cameras:
            self.add_camera(camera)

    def add_camera(self, camera: CameraModel) -> None:
        """
        Adds one camera to list.
        """

        self.cameras[camera.id] = camera

        self.camera_list.addItem(
            f"{camera.id}: {camera.name} [{camera.source}]"
        )

    def _on_camera_clicked(self, item) -> None:
        """
        Emits selected camera.
        """

        camera_id = int(item.text().split(":")[0])

        camera = self.cameras[camera_id]

        self.camera_selected.emit(camera)