from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class StatusPanel(QWidget):
    """
    OCR and session status panel.
    """

    def __init__(self) -> None:
        super().__init__()

        self.session_label = QLabel("Session: stopped")
        self.auto_ocr_label = QLabel("Auto OCR: stopped")
        self.ocr_label = QLabel("OCR: idle")
        self.camera_label = QLabel("Cameras: 0 active")
        self.last_result_label = QLabel("Last result: -")

        layout = QVBoxLayout()
        layout.addWidget(self.session_label)
        layout.addWidget(self.auto_ocr_label)
        layout.addWidget(self.ocr_label)
        layout.addWidget(self.camera_label)
        layout.addWidget(self.last_result_label)
        layout.addStretch()

        self.setLayout(layout)

    def set_session_status(self, text: str) -> None:
        self.session_label.setText(f"Session: {text}")

    def set_auto_ocr_status(self, text: str) -> None:
        self.auto_ocr_label.setText(f"Auto OCR: {text}")

    def set_ocr_status(self, text: str) -> None:
        self.ocr_label.setText(f"OCR: {text}")

    def set_camera_status(self, active_count: int) -> None:
        self.camera_label.setText(f"Cameras: {active_count} active")

    def set_last_result(self, text: str) -> None:
        self.last_result_label.setText(f"Last result: {text}")