import traceback

import numpy as np
from PySide6.QtCore import QThread, Signal

from app.models.roi_model import ROIModel
from app.ocr.ocr_pipeline import OCRPipeline


class OCRWorker(QThread):
    """
    Background OCR worker.

    Runs OCR processing outside the UI thread.
    """

    result_ready = Signal(object, object, float, object, str)

    error_occurred = Signal(str)

    def __init__(
        self,
        frame: np.ndarray,
        roi: ROIModel,
        debug_path: str,
    ) -> None:
        super().__init__()

        self.frame = frame.copy()
        self.roi = roi
        self.debug_path = debug_path

    def run(self) -> None:
        """
        Runs OCR processing.
        """

        try:
            ocr_pipeline = OCRPipeline()

            processed, raw_text, confidence, numeric_value = (
                ocr_pipeline.process_roi(
                    self.frame,
                    self.roi,
                )
            )

            ocr_pipeline.save_debug_image(
                processed,
                self.debug_path,
            )

            self.result_ready.emit(
                self.roi,
                raw_text,
                confidence,
                numeric_value,
                self.debug_path,
            )

        except Exception:
            self.error_occurred.emit(traceback.format_exc())