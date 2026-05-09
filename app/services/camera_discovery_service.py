import cv2


class CameraDiscoveryService:
    """
    Discovers available USB cameras on Windows.

    RTSP cameras cannot be reliably discovered automatically,
    because they require network address, login and password.
    """

    def discover_usb_cameras(
        self,
        max_index: int = 10,
    ) -> list[str]:
        """
        Returns available USB camera indexes as strings.
        """

        available_sources: list[str] = []

        for index in range(max_index):
            capture = cv2.VideoCapture(index, cv2.CAP_DSHOW)

            if capture.isOpened():
                success, _ = capture.read()

                if success:
                    available_sources.append(str(index))

            capture.release()

        return available_sources