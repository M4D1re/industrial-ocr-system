import numpy as np
from PySide6.QtCore import QObject, Signal

from app.models.camera_model import CameraModel
from app.services.camera_service import CameraService


class CameraManager(QObject):
    """
    Manages multiple camera services at the same time.
    """

    frame_ready = Signal(int, object)
    connection_changed = Signal(int, bool)
    fps_updated = Signal(int, float)

    def __init__(self) -> None:
        super().__init__()

        self.camera_services: dict[int, CameraService] = {}
        self.latest_frames: dict[int, np.ndarray] = {}

    def start_camera(self, camera: CameraModel) -> None:
        """
        Starts one camera if it is not already running.
        """

        if camera.id in self.camera_services:
            return

        camera_service = CameraService(camera.source)

        camera_service.frame_ready.connect(
            lambda frame, camera_id=camera.id: self._on_frame_ready(
                camera_id,
                frame,
            )
        )

        camera_service.connection_changed.connect(
            lambda connected, camera_id=camera.id: self.connection_changed.emit(
                camera_id,
                connected,
            )
        )

        camera_service.fps_updated.connect(
            lambda fps, camera_id=camera.id: self.fps_updated.emit(
                camera_id,
                fps,
            )
        )

        self.camera_services[camera.id] = camera_service

        camera_service.start()

    def start_cameras(self, cameras: list[CameraModel]) -> None:
        """
        Starts all enabled cameras.
        """

        for camera in cameras:
            if camera.enabled:
                self.start_camera(camera)

    def stop_camera(self, camera_id: int) -> None:
        """
        Stops one camera.
        """

        camera_service = self.camera_services.pop(camera_id, None)

        if camera_service is not None:
            camera_service.stop()

        self.latest_frames.pop(camera_id, None)

    def stop_all(self) -> None:
        """
        Stops all cameras.
        """

        for camera_id in list(self.camera_services.keys()):
            self.stop_camera(camera_id)

    def get_latest_frame(self, camera_id: int) -> np.ndarray | None:
        """
        Returns latest frame for camera.
        """

        frame = self.latest_frames.get(camera_id)

        if frame is None:
            return None

        return frame.copy()

    def _on_frame_ready(
        self,
        camera_id: int,
        frame: np.ndarray,
    ) -> None:
        """
        Stores latest frame and emits UI signal.
        """

        self.latest_frames[camera_id] = frame.copy()

        self.frame_ready.emit(camera_id, frame)