from pathlib import Path

from PySide6.QtWidgets import QMessageBox

from app.database.reading_repository import ReadingRepository

from app.ui.widgets.readings_panel import ReadingsPanel

from app.ui.dialogs.add_camera_dialog import AddCameraDialog



from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QLabel,
    QDockWidget,
    QMainWindow,
    QMessageBox,
    QSpinBox,
    QStatusBar,
    QToolBar,
)

from app.models.camera_model import CameraModel
from app.services.multi_camera_ocr_worker import (
    MultiCameraOCRWorker,
    OCRCameraTask,
)

from app.database.camera_repository import CameraRepository
from app.database.database_manager import DatabaseManager
from app.services.camera_discovery_service import CameraDiscoveryService
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

        self.reading_repository = ReadingRepository(self.database)

        self.ocr_worker: MultiCameraOCRWorker | None = None



        self.auto_ocr_enabled = False

        self.auto_ocr_timer = QTimer(self)

        self.auto_ocr_timer.timeout.connect(
            self._process_selected_roi
        )

        self.default_camera = (
            self.camera_repository.get_or_create_default_camera()
        )

        self.active_display_camera: CameraModel = self.default_camera

        self.setWindowTitle("Industrial OCR System")

        self.resize(1600, 900)

        self.camera_manager = CameraManager()

        self.camera_discovery_service = CameraDiscoveryService()

        self._setup_ui()

        self._discover_usb_cameras()

        self._load_saved_cameras()

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

        toolbar.addSeparator()

        toolbar.addWidget(QLabel("Hours:"))

        self.polling_hours_spinbox = QSpinBox()
        self.polling_hours_spinbox.setRange(0, 24)
        self.polling_hours_spinbox.setValue(0)
        toolbar.addWidget(self.polling_hours_spinbox)

        toolbar.addWidget(QLabel("Minutes:"))

        self.polling_minutes_spinbox = QSpinBox()
        self.polling_minutes_spinbox.setRange(0, 59)
        self.polling_minutes_spinbox.setValue(0)
        toolbar.addWidget(self.polling_minutes_spinbox)

        toolbar.addWidget(QLabel("Seconds:"))

        self.polling_seconds_spinbox = QSpinBox()
        self.polling_seconds_spinbox.setRange(1, 59)
        self.polling_seconds_spinbox.setValue(5)
        toolbar.addWidget(self.polling_seconds_spinbox)

        toolbar.addSeparator()

        start_auto_ocr_action = toolbar.addAction("Start Auto OCR")
        start_auto_ocr_action.triggered.connect(
            self._start_auto_ocr
        )

        stop_auto_ocr_action = toolbar.addAction("Stop Auto OCR")
        stop_auto_ocr_action.triggered.connect(
            self._stop_auto_ocr
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

        self._create_readings_dock()

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

        self.camera_panel = CameraPanel()

        self.camera_panel.add_camera_requested.connect(
            self._open_add_camera_dialog
        )

        self.camera_panel.camera_selected.connect(
            self._on_camera_selected
        )

        self.camera_panel.enable_camera_requested.connect(
            self._enable_camera
        )

        self.camera_panel.disable_camera_requested.connect(
            self._disable_camera
        )

        dock.setWidget(self.camera_panel)

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

        self.roi_panel.enable_requested.connect(
            self._enable_roi
        )

        self.roi_panel.disable_requested.connect(
            self._disable_roi
        )


        dock.setWidget(self.roi_panel)

        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

    def _create_readings_dock(self) -> None:
        """
        Creates current readings dock.
        """

        dock = QDockWidget("Current Readings", self)

        dock.setAllowedAreas(
            Qt.LeftDockWidgetArea |
            Qt.RightDockWidgetArea |
            Qt.BottomDockWidgetArea
        )

        self.readings_panel = ReadingsPanel()

        dock.setWidget(self.readings_panel)

        self.addDockWidget(Qt.RightDockWidgetArea, dock)

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

    def _open_add_camera_dialog(self) -> None:
        """
        Opens add camera dialog and saves camera.
        """

        dialog = AddCameraDialog()

        if dialog.exec() != dialog.Accepted:
            return

        name, source_type, source = dialog.get_camera_data()

        if not name:
            QMessageBox.warning(
                self,
                "Invalid camera",
                "Введите имя камеры.",
            )
            return

        if not source:
            QMessageBox.warning(
                self,
                "Invalid camera",
                "Введите источник камеры.",
            )
            return

        if source_type == "USB" and not source.isdigit():
            QMessageBox.warning(
                self,
                "Invalid USB source",
                "Для USB-камеры источник должен быть числом: 0, 1, 2...",
            )
            return

        if source_type == "RTSP" and not source.lower().startswith("rtsp://"):
            QMessageBox.warning(
                self,
                "Invalid RTSP URL",
                "RTSP-адрес должен начинаться с rtsp://",
            )
            return

        camera = self.camera_repository.create(
            name=name,
            source=source,
            enabled=True,
        )

        self.camera_panel.add_camera(camera)

        self.statusBar().showMessage(
            f"Camera added: {camera.name} [{camera.source}]"
        )

    def _on_camera_selected(self, camera) -> None:
        """
        Selects camera for display only.
        """

        self.active_display_camera = camera

        self._load_saved_roi_regions()

        latest_frame = self.camera_manager.get_latest_frame(camera.id)

        if latest_frame is not None:
            self.video_widget.update_cv_frame(latest_frame)

            image = FrameConverter.convert_cv_to_qt(latest_frame)

            self.video_widget.update_frame(image)

        self.statusBar().showMessage(
            f"Displaying camera: {camera.name} [{camera.source}]"
        )

    def _discover_usb_cameras(self) -> None:
        """
        Discovers available USB cameras and saves them to database.
        """

        sources = self.camera_discovery_service.discover_usb_cameras(
            max_index=10
        )

        for source in sources:
            self.camera_repository.create(
                name=f"USB Camera {source}",
                source=source,
                enabled=True,
            )

        self.statusBar().showMessage(
            f"Discovered USB cameras: {len(sources)}"
        )

    def _load_saved_cameras(self) -> None:
        """
        Loads cameras from database into camera panel.
        """

        cameras = self.camera_repository.list_all()

        self.camera_panel.set_cameras(cameras)

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
        Starts all enabled cameras.
        """

        cameras = self.camera_repository.list_all()

        self.camera_manager.frame_ready.connect(
            self._on_frame_ready
        )

        self.camera_manager.connection_changed.connect(
            self._on_camera_connection_changed
        )

        self.camera_manager.fps_updated.connect(
            self._on_fps_updated
        )

        self.camera_manager.start_cameras(cameras)

    def _on_frame_ready(
            self,
            camera_id: int,
            frame,
    ) -> None:
        """
        Receives camera frame.

        Only selected camera is displayed,
        but all cameras continue working in background.
        """

        if camera_id != self.active_display_camera.id:
            return

        self.video_widget.update_cv_frame(frame)

        image = FrameConverter.convert_cv_to_qt(frame)

        self.video_widget.update_frame(image)

    def _on_camera_connection_changed(
            self,
            camera_id: int,
            connected: bool,
    ) -> None:
        """
        Updates camera connection status.
        """

        status = "connected" if connected else "disconnected"

        self.statusBar().showMessage(
            f"Camera {camera_id}: {status}"
        )

    def _on_fps_updated(
            self,
            camera_id: int,
            fps: float,
    ) -> None:
        """
        Updates FPS status for selected camera.
        """

        if camera_id != self.active_display_camera.id:
            return

        self.statusBar().showMessage(
            f"Camera {camera_id} | FPS: {fps:.2f}"
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

    def _start_auto_ocr(self) -> None:
        """
        Starts automatic OCR polling.
        """

        if not self.video_widget.roi_regions:
            QMessageBox.warning(
                self,
                "No ROI",
                "Сначала выдели хотя бы одну ROI-область.",
            )
            return

        hours = self.polling_hours_spinbox.value()
        minutes = self.polling_minutes_spinbox.value()
        seconds = self.polling_seconds_spinbox.value()

        total_seconds = hours * 3600 + minutes * 60 + seconds

        if total_seconds <= 0:
            QMessageBox.warning(
                self,
                "Invalid interval",
                "Периодичность должна быть больше 0 секунд.",
            )
            return

        self.auto_ocr_enabled = True

        self.auto_ocr_timer.start(total_seconds * 1000)

        self.statusBar().showMessage(
            f"Auto OCR started. Interval: {total_seconds} sec"
        )

    def _stop_auto_ocr(self) -> None:
        """
        Stops automatic OCR polling.
        """

        self.auto_ocr_enabled = False

        self.auto_ocr_timer.stop()

        self.statusBar().showMessage("Auto OCR stopped")

    def _enable_camera(self, camera_id: int) -> None:
        """
        Enables camera and starts its stream.
        """

        self.camera_repository.set_enabled(camera_id, True)

        cameras = self.camera_repository.list_all()

        self.camera_panel.set_cameras(cameras)

        camera = next(
            item for item in cameras if item.id == camera_id
        )

        self.camera_manager.start_camera(camera)

        self.statusBar().showMessage(
            f"Camera enabled: {camera.name}"
        )

    def _disable_camera(self, camera_id: int) -> None:
        """
        Disables camera and stops its stream.
        """

        self.camera_repository.set_enabled(camera_id, False)

        self.camera_manager.stop_camera(camera_id)

        cameras = self.camera_repository.list_all()

        self.camera_panel.set_cameras(cameras)

        self.statusBar().showMessage(
            f"Camera disabled: {camera_id}"
        )

    def _enable_roi(self, roi_id: int) -> None:
        """
        Enables ROI.
        """

        self.roi_repository.set_enabled(roi_id, True)

        self._load_saved_roi_regions()

        self.statusBar().showMessage(
            f"ROI enabled: {roi_id}"
        )

    def _disable_roi(self, roi_id: int) -> None:
        """
        Disables ROI.
        """

        self.roi_repository.set_enabled(roi_id, False)

        self._load_saved_roi_regions()

        self.statusBar().showMessage(
            f"ROI disabled: {roi_id}"
        )


    def _process_selected_roi(self) -> None:
        """
        Starts OCR processing for all enabled cameras and enabled ROI regions.
        """

        if self.ocr_worker is not None and self.ocr_worker.isRunning():
            if self.auto_ocr_enabled:
                self.statusBar().showMessage(
                    "OCR is still running. Auto tick skipped."
                )
            else:
                QMessageBox.information(
                    self,
                    "OCR is running",
                    "OCR уже выполняется. Дождись завершения.",
                )

            return

        cameras = [
            camera
            for camera in self.camera_repository.list_all()
            if camera.enabled
        ]

        tasks: list[OCRCameraTask] = []

        for camera in cameras:
            frame = self.camera_manager.get_latest_frame(camera.id)

            if frame is None:
                continue

            roi_regions = self.roi_repository.list_enabled_by_camera(
                camera.id
            )

            if not roi_regions:
                continue

            tasks.append(
                OCRCameraTask(
                    camera=camera,
                    frame=frame,
                    roi_regions=roi_regions,
                )
            )

        if not tasks:
            if not self.auto_ocr_enabled:
                QMessageBox.warning(
                    self,
                    "No OCR tasks",
                    "Нет активных камер с кадрами и включенными ROI.",
                )

            self.statusBar().showMessage("No OCR tasks available")
            return

        debug_dir = Path("data/debug")
        debug_dir.mkdir(parents=True, exist_ok=True)

        roi_count = sum(len(task.roi_regions) for task in tasks)

        self.statusBar().showMessage(
            f"OCR started: {len(tasks)} cameras, {roi_count} ROI"
        )

        self.ocr_worker = MultiCameraOCRWorker(
            tasks=tasks,
            debug_dir=str(debug_dir),
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
            camera,
            roi,
            raw_text,
            confidence: float,
            numeric_value,
            debug_path: str,
    ) -> None:
        """
        Handles OCR result from multi-camera worker.
        """

        self.statusBar().showMessage(
            f"OCR completed: {camera.name} / {roi.name}"
        )

        reading_id = self.reading_repository.create(
            roi_id=roi.id,
            value=numeric_value,
            raw_text=raw_text,
            confidence=confidence,
        )

        self.readings_panel.update_reading(
            reading_id=reading_id,
            roi_name=f"{camera.name} / {roi.name}",
            value=numeric_value,
            raw_text=raw_text,
            confidence=confidence,
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