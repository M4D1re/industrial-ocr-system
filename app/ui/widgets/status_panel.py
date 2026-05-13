from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class StatusPanel(QWidget):
    """
    OCR and session status panel.
    """

    def __init__(self) -> None:
        super().__init__()

        self.session_label = QLabel()
        self.auto_ocr_label = QLabel()
        self.ocr_label = QLabel()
        self.camera_label = QLabel()
        self.last_result_label = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.session_label)
        layout.addWidget(self.auto_ocr_label)
        layout.addWidget(self.ocr_label)
        layout.addWidget(self.camera_label)
        layout.addWidget(self.last_result_label)
        layout.addStretch()

        self.setLayout(layout)

        self.set_session_status("stopped")
        self.set_auto_ocr_status("stopped")
        self.set_ocr_status("idle")
        self.set_camera_status(0)
        self.set_last_result("-")

    def _set_colored_text(
        self,
        label: QLabel,
        title: str,
        value: str,
        color: str,
    ) -> None:
        label.setText(
            (
                f"<b style='color:#94a3b8;'>{title}:</b> "
                f"<span style='color:{color}; font-weight:600;'>{value}</span>"
            )
        )

    def set_session_status(self, text: str) -> None:
        color = "#22c55e" if "active" in text else "#f87171"
        self._set_colored_text(self.session_label, "Session", text, color)

    def set_auto_ocr_status(self, text: str) -> None:
        color = "#22c55e" if "running" in text else "#f87171"
        self._set_colored_text(self.auto_ocr_label, "Auto OCR", text, color)

    def set_ocr_status(self, text: str) -> None:
        if "error" in text:
            color = "#ef4444"
        elif "running" in text:
            color = "#facc15"
        else:
            color = "#22c55e"

        self._set_colored_text(self.ocr_label, "OCR", text, color)

    def set_camera_status(self, active_count: int) -> None:
        color = "#22c55e" if active_count > 0 else "#f87171"
        self._set_colored_text(
            self.camera_label,
            "Cameras",
            f"{active_count} active",
            color,
        )

    def set_last_result(self, text: str) -> None:
        self._set_colored_text(
            self.last_result_label,
            "Last result",
            text,
            "#60a5fa",
        )