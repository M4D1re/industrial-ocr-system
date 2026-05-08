from app.services.camera_service import CameraService


class CameraManager:
    """
    Manages all camera services.
    """

    def __init__(self) -> None:
        self.cameras: list[CameraService] = []

    def add_camera(self, source: str) -> CameraService:
        """
        Creates and starts camera.
        """

        camera = CameraService(source)

        self.cameras.append(camera)

        camera.start()

        return camera

    def stop_all(self) -> None:
        """
        Stops all cameras.
        """

        for camera in self.cameras:
            camera.stop()