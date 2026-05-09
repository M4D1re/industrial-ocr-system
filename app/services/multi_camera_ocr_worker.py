import traceback
from dataclasses import dataclass

import numpy as np
from PySide6.QtCore import QThread, Signal

from app.models.camera_model import CameraModel
from app.models.roi_model import ROIModel
from app.ocr.ocr_pipeline import OCRPipeline


@dataclass
class OCRCameraTask:
    """
    OCR task for one camera.
    """

    camera: CameraModel
    frame: np.ndarray
    roi_regions: list[ROIModel]


class MultiCameraOCRWorker(QThread):
    """
    Processes OCR for multiple cameras and their ROI regions.
    """

    result_ready = Signal(object, object, object, float, object, str)
    error_occurred = Signal(str)

    def __init__(
        self,
        tasks: list[OCRCameraTask],
        debug_dir: str,
    ) -> None:
        super().__init__()

        self.tasks = tasks
        self.debug_dir = debug_dir

    def run(self) -> None:
        """
        Runs OCR for all tasks.
        """

        try:
            ocr_pipeline = OCRPipeline()

            for task in self.tasks:
                for roi in task.roi_regions:
                    processed, raw_text, confidence, numeric_value = (
                        ocr_pipeline.process_roi(
                            task.frame,
                            roi,
                        )
                    )

                    debug_path = (
                        f"{self.debug_dir}/camera_{task.camera.id}"
                        f"_roi_{roi.id}_processed.png"
                    )

                    ocr_pipeline.save_debug_image(
                        processed,
                        debug_path,
                    )

                    self.result_ready.emit(
                        task.camera,
                        roi,
                        raw_text,
                        confidence,
                        numeric_value,
                        debug_path,
                    )

        except Exception:
            self.error_occurred.emit(traceback.format_exc())