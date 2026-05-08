from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QPushButton,
    QListWidget,
    QVBoxLayout,
    QWidget,
)

from app.models.roi_model import ROIModel


class ROIPanel(QWidget):
    """
    Panel with selected ROI regions.
    """

    delete_requested = Signal(int)

    def __init__(self) -> None:
        super().__init__()

        self.roi_items: dict[int, ROIModel] = {}

        self.roi_list = QListWidget()

        self.delete_button = QPushButton("Delete selected ROI")

        self.delete_button.clicked.connect(self._on_delete_clicked)

        layout = QVBoxLayout()

        layout.addWidget(self.roi_list)

        layout.addWidget(self.delete_button)

        self.setLayout(layout)

    def add_roi(self, roi: ROIModel) -> None:
        """
        Adds ROI to list.
        """

        self.roi_items[roi.id] = roi

        self.roi_list.addItem(
            f"{roi.id}: {roi.name} "
            f"({roi.x}, {roi.y}, {roi.width}x{roi.height})"
        )

    def remove_roi(self, roi_id: int) -> None:
        """
        Removes ROI from list.
        """

        self.roi_items.pop(roi_id, None)

        for index in range(self.roi_list.count()):
            item = self.roi_list.item(index)

            if item.text().startswith(f"{roi_id}:"):
                self.roi_list.takeItem(index)
                break

    def _on_delete_clicked(self) -> None:
        """
        Emits selected ROI delete request.
        """

        selected_items = self.roi_list.selectedItems()

        if not selected_items:
            return

        selected_text = selected_items[0].text()

        roi_id = int(selected_text.split(":")[0])

        self.delete_requested.emit(roi_id)