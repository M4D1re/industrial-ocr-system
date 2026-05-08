from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDockWidget,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
)

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

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Industrial OCR System")

        self.resize(1600, 900)

        self.camera_manager = CameraManager()

        self._setup_ui()

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

        self.setCentralWidget(self.video_widget)

    def _create_docks(self) -> None:
        """
        Creates docking panels.
        """

        self._create_camera_dock()

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

    def _initialize_test_camera(self) -> None:
        """
        Initializes default test camera.

        Source '0' means the default webcam connected to the computer.
        """

        camera = self.camera_manager.add_camera("0")

        camera.frame_ready.connect(self._on_frame_ready)

        camera.connection_changed.connect(
            self._on_camera_connection_changed
        )

        camera.fps_updated.connect(self._on_fps_updated)

    def _on_frame_ready(self, frame) -> None:
        """
        Receives camera frame from background camera thread.
        """

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

    def closeEvent(self, event) -> None:
        """
        Stops camera threads before application closes.
        """

        self.camera_manager.stop_all()

        event.accept()