import os

import cv2


class CameraDiscoveryService:
    """
    Discovers available USB cameras on Windows.
    """

    def discover_usb_cameras(
        self,
        max_index: int = 5,
    ) -> list[str]:
        """
        Returns available USB camera indexes as strings.
        """

        os.environ["OPENCV_LOG_LEVEL"] = "SILENT"

        available_sources: list[str] = []

        for index in range(max_index):
            capture = cv2.VideoCapture(index)

            if not capture.isOpened():
                capture.release()
                continue

            success, _ = capture.read()

            capture.release()

            if success:
                available_sources.append(str(index))

        return available_sources