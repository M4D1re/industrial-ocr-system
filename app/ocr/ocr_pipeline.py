import cv2
import numpy as np

from app.models.roi_model import ROIModel
from app.ocr.ocr_engine import OCREngine
from app.vision.vision_processor import VisionProcessor


class OCRPipeline:
    """
    Full OCR pipeline:
    crop ROI -> preprocess -> OCR -> parse number.
    """

    def __init__(self) -> None:
        self.ocr_engine = OCREngine()

    def process_roi(
        self,
        frame: np.ndarray,
        roi: ROIModel,
    ) -> tuple[np.ndarray, str, float, float | None]:
        """
        Processes one ROI.

        Returns:
            processed image,
            raw OCR text,
            confidence,
            parsed numeric value.
        """

        cropped = VisionProcessor.crop_roi(frame, roi)

        if cropped.size == 0:
            raise ValueError("ROI crop is empty")

        processed = VisionProcessor.preprocess_for_ocr(cropped)

        raw_text, confidence = self.ocr_engine.recognize(processed)

        numeric_value = self.ocr_engine.extract_number(raw_text)

        return processed, raw_text, confidence, numeric_value

    def save_debug_image(
        self,
        image: np.ndarray,
        path: str,
    ) -> None:
        """
        Saves processed ROI image for debugging.
        """

        cv2.imwrite(path, image)