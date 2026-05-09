from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

import cv2


class AddCameraDialog(QDialog):
    """
    Dialog for adding USB or RTSP camera manually.
    """

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Add Camera")
        self.resize(520, 180)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Например: Цех 1 — станок 3")

        self.source_type_input = QComboBox()
        self.source_type_input.addItems(["USB", "RTSP"])
        self.source_type_input.currentTextChanged.connect(
            self._on_source_type_changed
        )

        self.source_input = QLineEdit()
        self.source_input.setPlaceholderText("USB индекс: 0, 1, 2...")

        self.test_button = QPushButton("Test connection")
        self.test_button.clicked.connect(self._test_connection)

        form = QFormLayout()
        form.addRow("Camera name:", self.name_input)
        form.addRow("Source type:", self.source_type_input)
        form.addRow("Source:", self.source_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok |
            QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.test_button)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def _on_source_type_changed(self, source_type: str) -> None:
        """
        Updates placeholder depending on source type.
        """

        if source_type == "USB":
            self.source_input.setPlaceholderText("USB индекс: 0, 1, 2...")
        else:
            self.source_input.setPlaceholderText(
                "rtsp://login:password@192.168.1.100:554/stream"
            )

    def _test_connection(self) -> None:
        """
        Tests camera connection.
        """

        source = self.source_input.text().strip()

        if not source:
            QMessageBox.warning(
                self,
                "Empty source",
                "Введите источник камеры.",
            )
            return

        if source.isdigit():
            video_source = int(source)
        else:
            video_source = source

        capture = cv2.VideoCapture(video_source, cv2.CAP_DSHOW)

        if not capture.isOpened():
            capture.release()

            capture = cv2.VideoCapture(video_source)

        success, _ = capture.read()

        capture.release()

        if success:
            QMessageBox.information(
                self,
                "Connection OK",
                "Камера успешно подключилась.",
            )
        else:
            QMessageBox.critical(
                self,
                "Connection failed",
                "Не удалось получить кадр с камеры.",
            )

    def get_camera_data(self) -> tuple[str, str, str]:
        """
        Returns camera name, source type and source.
        """

        name = self.name_input.text().strip()
        source_type = self.source_type_input.currentText().strip()
        source = self.source_input.text().strip()

        return name, source_type, source