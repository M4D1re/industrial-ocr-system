from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
)


class AddCameraDialog(QDialog):
    """
    Dialog for adding USB or RTSP camera.
    """

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Add Camera")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Example: Camera 1")

        self.source_type_input = QComboBox()
        self.source_type_input.addItems(
            [
                "USB",
                "RTSP",
            ]
        )

        self.source_input = QLineEdit()
        self.source_input.setPlaceholderText(
            "USB: 0, 1, 2... or RTSP URL"
        )

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

        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_camera_data(self) -> tuple[str, str]:
        """
        Returns camera name and source.
        """

        name = self.name_input.text().strip()

        source = self.source_input.text().strip()

        return name, source