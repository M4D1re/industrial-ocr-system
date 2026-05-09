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
    enable_camera_requested = Signal(int)
    disable_camera_requested = Signal(int)

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

        self.enable_button = QPushButton("Enable selected camera")
        self.enable_button.clicked.connect(
            self._on_enable_clicked
        )

        self.disable_button = QPushButton("Disable selected camera")
        self.disable_button.clicked.connect(
            self._on_disable_clicked
        )

        layout.addWidget(title)
        layout.addWidget(self.camera_list)
        layout.addWidget(self.add_camera_button)
        layout.addWidget(self.enable_button)
        layout.addWidget(self.disable_button)

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

        status = "ON" if camera.enabled else "OFF"

        self.camera_list.addItem(
            f"{camera.id}: {camera.name} [{camera.source}] ({status})"
        )

    def update_camera(self, camera: CameraModel) -> None:
        """
        Updates camera in list.
        """

        self.cameras[camera.id] = camera

        self.set_cameras(list(self.cameras.values()))

    def get_selected_camera_id(self) -> int | None:
        """
        Returns selected camera id.
        """

        selected_items = self.camera_list.selectedItems()

        if not selected_items:
            return None

        selected_text = selected_items[0].text()

        return int(selected_text.split(":")[0])

    def _on_camera_clicked(self, item) -> None:
        """
        Emits selected camera.
        """

        camera_id = int(item.text().split(":")[0])

        camera = self.cameras[camera_id]

        self.camera_selected.emit(camera)

    def _on_enable_clicked(self) -> None:
        """
        Emits enable camera request.
        """

        camera_id = self.get_selected_camera_id()

        if camera_id is not None:
            self.enable_camera_requested.emit(camera_id)

    def _on_disable_clicked(self) -> None:
        """
        Emits disable camera request.
        """

        camera_id = self.get_selected_camera_id()

        if camera_id is not None:
            self.disable_camera_requested.emit(camera_id)