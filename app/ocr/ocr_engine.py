import re

import cv2
import numpy as np
from paddleocr import PaddleOCR


class OCREngine:
    """
    PaddleOCR wrapper.
    """

    def __init__(self) -> None:
        self.engine = PaddleOCR(
            lang="en",
            device="cpu",
        )

    def recognize(self, image: np.ndarray) -> tuple[str, float]:
        """
        Recognizes text from image.

        Returns:
            text and confidence.
        """

        ocr_image = self._prepare_image_for_paddleocr(image)

        result = self.engine.predict(ocr_image)

        if not result:
            return "", 0.0

        texts: list[str] = []
        confidences: list[float] = []

        for item in result:
            item_dict = dict(item)

            recognized_texts = item_dict.get("rec_texts", [])
            recognized_scores = item_dict.get("rec_scores", [])

            for text in recognized_texts:
                texts.append(str(text))

            for score in recognized_scores:
                confidences.append(float(score))

        if not texts:
            return "", 0.0

        full_text = " ".join(texts)

        avg_confidence = (
            sum(confidences) / len(confidences)
            if confidences
            else 0.0
        )

        return full_text, avg_confidence

    @staticmethod
    def _prepare_image_for_paddleocr(image: np.ndarray) -> np.ndarray:
        """
        Converts image to PaddleOCR-compatible format.

        PaddleOCR expects a normal 3-channel image.
        Our preprocessing returns a 2D black-white image,
        so we convert it back to BGR.
        """

        if image.ndim == 2:
            return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        if image.ndim == 3 and image.shape[2] == 1:
            return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        return image

    @staticmethod
    def extract_number(text: str) -> float | None:
        """
        Extracts first decimal/negative number from OCR text.
        """

        cleaned = text.replace(",", ".")

        match = re.search(r"-?\d+(?:\.\d+)?", cleaned)

        if not match:
            return None

        return float(match.group(0))