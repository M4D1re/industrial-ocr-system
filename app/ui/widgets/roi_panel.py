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
    enable_requested = Signal(int)
    disable_requested = Signal(int)

    def __init__(self) -> None:
        super().__init__()

        self.roi_items: dict[int, ROIModel] = {}

        self.roi_list = QListWidget()

        self.delete_button = QPushButton("Delete selected ROI")
        self.delete_button.clicked.connect(self._on_delete_clicked)

        self.enable_button = QPushButton("Enable selected ROI")
        self.enable_button.clicked.connect(self._on_enable_clicked)

        self.disable_button = QPushButton("Disable selected ROI")
        self.disable_button.clicked.connect(self._on_disable_clicked)

        layout = QVBoxLayout()

        layout.addWidget(self.roi_list)
        layout.addWidget(self.enable_button)
        layout.addWidget(self.disable_button)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

    def add_roi(self, roi: ROIModel) -> None:
        """
        Adds ROI to list.
        """

        self.roi_items[roi.id] = roi

        status = "ON" if roi.enabled else "OFF"

        self.roi_list.addItem(
            f"{roi.id}: {roi.name} "
            f"({roi.x}, {roi.y}, {roi.width}x{roi.height}) "
            f"({status})"
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

    def update_roi(self, roi: ROIModel) -> None:
        """
        Updates ROI list item.
        """

        self.roi_items[roi.id] = roi

        self.clear()

        for item in self.roi_items.values():
            self.add_roi(item)

    def clear(self) -> None:
        """
        Clears ROI list.
        """

        self.roi_items.clear()
        self.roi_list.clear()

    def get_selected_roi_id(self) -> int | None:
        """
        Returns selected ROI id.
        """

        selected_items = self.roi_list.selectedItems()

        if not selected_items:
            return None

        selected_text = selected_items[0].text()

        return int(selected_text.split(":")[0])

    def _on_delete_clicked(self) -> None:
        """
        Emits selected ROI delete request.
        """

        roi_id = self.get_selected_roi_id()

        if roi_id is not None:
            self.delete_requested.emit(roi_id)

    def _on_enable_clicked(self) -> None:
        """
        Emits enable ROI request.
        """

        roi_id = self.get_selected_roi_id()

        if roi_id is not None:
            self.enable_requested.emit(roi_id)

    def _on_disable_clicked(self) -> None:
        """
        Emits disable ROI request.
        """

        roi_id = self.get_selected_roi_id()

        if roi_id is not None:
            self.disable_requested.emit(roi_id)