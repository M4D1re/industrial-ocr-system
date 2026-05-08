import cv2
import numpy as np

from app.models.roi_model import ROIModel
from app.vision.vision_processor import VisionProcessor


class OCRPipeline:
    """
    OCR pipeline foundation.

    For now it only crops and preprocesses ROI.
    PaddleOCR recognition will be added later.
    """

    def process_roi(
        self,
        frame: np.ndarray,
        roi: ROIModel,
    ) -> np.ndarray:
        """
        Processes one ROI and returns preprocessed image.
        """

        cropped = VisionProcessor.crop_roi(frame, roi)

        if cropped.size == 0:
            raise ValueError("ROI crop is empty")

        processed = VisionProcessor.preprocess_for_ocr(cropped)

        return processed

    def save_debug_image(
        self,
        image: np.ndarray,
        path: str,
    ) -> None:
        """
        Saves processed ROI image for debugging.
        """

        cv2.imwrite(path, image)