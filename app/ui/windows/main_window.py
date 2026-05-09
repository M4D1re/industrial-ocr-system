from pathlib import Path

from PySide6.QtWidgets import QMessageBox


from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDockWidget,
    QMainWindow,
    QMessageBox,
    QStatusBar,
    QToolBar,
)

from app.services.ocr_worker import OCRWorker

from app.database.camera_repository import CameraRepository
from app.database.database_manager import DatabaseManager
from app.database.roi_repository import ROIRepository

from app.ui.widgets.roi_panel import ROIPanel

from app.services.camera_manager import CameraManager
from app.vision.frame_converter import FrameConverter

from app.ui.widgets.analytics_panel import AnalyticsPanel
from app.ui.widgets.camera_panel import CameraPanel
from app.ui.widgets.logs_panel import LogsPanel
from app.ui.widgets.status_panel import StatusPanel
from app.ui.widgets.video_widget import VideoWidget


class MainWindow(QMainWindow):
    """
    Main application window.
    """

    def __init__(self, database: DatabaseManager) -> None:
        super().__init__()

        self.database = database

        self.camera_repository = CameraRepository(self.database)

        self.roi_repository = ROIRepository(self.database)


        self.ocr_worker: OCRWorker | None = None

        self.default_camera = (
            self.camera_repository.get_or_create_default_camera()
        )

        self.setWindowTitle("Industrial OCR System")

        self.resize(1600, 900)

        self.camera_manager = CameraManager()

        self._setup_ui()

        self._load_saved_roi_regions()

        self._initialize_test_camera()

    def _setup_ui(self) -> None:
        """
        Initializes main UI.
        """

        self._create_toolbar()

        self._create_statusbar()

        self._create_central_video()

        self._create_docks()

    def _create_toolbar(self) -> None:
        """
        Creates top toolbar.
        """

        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)

        process_roi_action = toolbar.addAction("Process ROI")

        process_roi_action.triggered.connect(
            self._process_selected_roi
        )

        self.addToolBar(toolbar)

    def _create_statusbar(self) -> None:
        """
        Creates bottom status bar.
        """

        statusbar = QStatusBar()

        statusbar.showMessage("System initialized")

        self.setStatusBar(statusbar)

    def _create_central_video(self) -> None:
        """
        Creates central video widget.
        """

        self.video_widget = VideoWidget()

        self.video_widget.roi_created.connect(
            self._on_roi_created
        )

        self.video_widget.roi_deleted.connect(
            self._on_roi_deleted
        )

        self.setCentralWidget(self.video_widget)



    def _create_docks(self) -> None:
        """
        Creates docking panels.
        """

        self._create_camera_dock()

        self._create_roi_dock()

        self._create_logs_dock()

        self._create_analytics_dock()

        self._create_status_dock()

    def _create_camera_dock(self) -> None:
        """
        Creates camera dock.
        """

        dock = QDockWidget("Cameras", self)

        dock.setAllowedAreas(
            Qt.LeftDockWidgetArea |
            Qt.RightDockWidgetArea
        )

        dock.setWidget(CameraPanel())

        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

    def _create_roi_dock(self) -> None:
        """
        Creates ROI dock.
        """

        dock = QDockWidget("ROI Regions", self)

        dock.setAllowedAreas(
            Qt.LeftDockWidgetArea |
            Qt.RightDockWidgetArea
        )

        self.roi_panel = ROIPanel()

        self.roi_panel.delete_requested.connect(
            self.video_widget.delete_roi
        )

        dock.setWidget(self.roi_panel)

        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

    def _create_logs_dock(self) -> None:
        """
        Creates logs dock.
        """

        dock = QDockWidget("Logs", self)

        dock.setWidget(LogsPanel())

        self.addDockWidget(Qt.BottomDockWidgetArea, dock)

    def _create_analytics_dock(self) -> None:
        """
        Creates analytics dock.
        """

        dock = QDockWidget("Analytics", self)

        dock.setWidget(AnalyticsPanel())

        self.addDockWidget(Qt.RightDockWidgetArea, dock)

    def _create_status_dock(self) -> None:
        """
        Creates OCR status dock.
        """

        dock = QDockWidget("OCR Status", self)

        dock.setWidget(StatusPanel())

        self.addDockWidget(Qt.RightDockWidgetArea, dock)

    def _load_saved_roi_regions(self) -> None:
        """
        Loads saved ROI regions from database.
        """

        roi_regions = self.roi_repository.list_by_camera(
            self.default_camera.id
        )

        self.video_widget.set_roi_regions(roi_regions)

        for roi in roi_regions:
            self.roi_panel.add_roi(roi)

        self.statusBar().showMessage(
            f"Loaded ROI regions: {len(roi_regions)}"
        )

    def _initialize_test_camera(self) -> None:
        """
        Initializes default test camera.
        """

        camera = self.camera_manager.add_camera(
            self.default_camera.source
        )

        camera.frame_ready.connect(self._on_frame_ready)

        camera.connection_changed.connect(
            self._on_camera_connection_changed
        )

        camera.fps_updated.connect(self._on_fps_updated)

    def _on_frame_ready(self, frame) -> None:
        """
        Receives camera frame from background camera thread.
        """

        self.video_widget.update_cv_frame(frame)

        image = FrameConverter.convert_cv_to_qt(frame)

        self.video_widget.update_frame(image)

    def _on_camera_connection_changed(
            self,
            connected: bool,
    ) -> None:
        """
        Updates UI when camera connection status changes.
        """

        if connected:
            self.statusBar().showMessage("Camera connected")
        else:
            self.statusBar().showMessage("Camera disconnected")

    def _on_fps_updated(self, fps: float) -> None:
        """
        Updates bottom status bar with current FPS.
        """

        self.statusBar().showMessage(
            f"Live Stream | FPS: {fps:.2f}"
        )

    def _on_roi_created(self, roi) -> None:
        """
        Handles new ROI creation and saves it to database.
        """

        database_roi_id = self.roi_repository.create(
            self.default_camera.id,
            roi,
        )

        roi.id = database_roi_id
        roi.name = f"ROI {database_roi_id}"

        self.roi_panel.add_roi(roi)

        self.statusBar().showMessage(
            f"ROI saved: {roi.name}"
        )

    def _on_roi_deleted(self, roi_id: int) -> None:
        """
        Handles ROI deletion and removes it from database.
        """

        self.roi_repository.delete(roi_id)

        self.roi_panel.remove_roi(roi_id)

        self.statusBar().showMessage(
            f"ROI deleted: {roi_id}"
        )

    def _process_selected_roi(self) -> None:
        """
        Starts OCR processing in background thread.
        """

        if self.ocr_worker is not None and self.ocr_worker.isRunning():
            QMessageBox.information(
                self,
                "OCR is running",
                "OCR уже выполняется. Дождись завершения.",
            )
            return

        if self.video_widget.last_cv_frame is None:
            QMessageBox.warning(
                self,
                "No frame",
                "Кадр с камеры еще не получен.",
            )
            return

        if not self.video_widget.roi_regions:
            QMessageBox.warning(
                self,
                "No ROI",
                "Сначала выдели хотя бы одну ROI-область.",
            )
            return

        roi = self.video_widget.roi_regions[0]

        debug_dir = Path("data/debug")
        debug_dir.mkdir(parents=True, exist_ok=True)

        debug_path = debug_dir / f"roi_{roi.id}_processed.png"

        self.statusBar().showMessage(
            f"OCR processing started for {roi.name}..."
        )

        self.ocr_worker = OCRWorker(
            self.video_widget.last_cv_frame,
            roi,
            str(debug_path),
        )

        self.ocr_worker.result_ready.connect(
            self._on_ocr_result_ready
        )

        self.ocr_worker.error_occurred.connect(
            self._on_ocr_error
        )

        self.ocr_worker.finished.connect(
            self._on_ocr_finished
        )

        self.ocr_worker.start()

    def _on_ocr_result_ready(
            self,
            roi,
            raw_text,
            confidence: float,
            numeric_value,
            debug_path: str,
    ) -> None:
        """
        Handles OCR result from background worker.
        """

        self.statusBar().showMessage(
            f"OCR completed for {roi.name}"
        )

        QMessageBox.information(
            self,
            "OCR result",
            (
                f"ROI: {roi.name}\n"
                f"Raw text: {raw_text}\n"
                f"Confidence: {confidence:.2f}\n"
                f"Numeric value: {numeric_value}\n\n"
                f"Debug image:\n{debug_path}"
            ),
        )

    def _on_ocr_error(self, error_text: str) -> None:
        """
        Handles OCR worker error.
        """

        self.statusBar().showMessage("OCR error")

        QMessageBox.critical(
            self,
            "OCR error",
            error_text,
        )

    def _on_ocr_finished(self) -> None:
        """
        Handles OCR worker finish.
        """

        self.statusBar().showMessage("OCR worker finished")

    def closeEvent(self, event) -> None:
        """
        Stops camera threads before application closes.
        """

        self.camera_manager.stop_all()

        event.accept()