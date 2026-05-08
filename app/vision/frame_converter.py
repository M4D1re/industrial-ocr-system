import cv2

from PySide6.QtGui import QImage


class FrameConverter:
    """
    Converts OpenCV frames to Qt images.
    """

    @staticmethod
    def convert_cv_to_qt(frame) -> QImage:
        """
        Converts OpenCV BGR frame to QImage.
        """

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        height, width, channels = rgb_frame.shape

        bytes_per_line = channels * width

        return QImage(
            rgb_frame.data,
            width,
            height,
            bytes_per_line,
            QImage.Format_RGB888,
        )