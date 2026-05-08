import cv2
import numpy as np

from app.models.roi_model import ROIModel


class VisionProcessor:
    """
    Handles computer vision operations before OCR.
    """

    @staticmethod
    def crop_roi(frame: np.ndarray, roi: ROIModel) -> np.ndarray:
        """
        Crops ROI area from full camera frame.
        """

        height, width = frame.shape[:2]

        x1 = max(0, roi.x)
        y1 = max(0, roi.y)
        x2 = min(width, roi.x + roi.width)
        y2 = min(height, roi.y + roi.height)

        return frame[y1:y2, x1:x2]

    @staticmethod
    def preprocess_for_ocr(image: np.ndarray) -> np.ndarray:
        """
        Prepares cropped ROI image for OCR.
        """

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        denoised = cv2.GaussianBlur(gray, (3, 3), 0)

        threshold = cv2.adaptiveThreshold(
            denoised,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            2,
        )

        resized = cv2.resize(
            threshold,
            None,
            fx=2,
            fy=2,
            interpolation=cv2.INTER_CUBIC,
        )

        return resized