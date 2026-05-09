from PySide6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class ReadingsPanel(QWidget):
    """
    Panel with latest OCR readings.
    """

    def __init__(self) -> None:
        super().__init__()

        self.table = QTableWidget()

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels(
            [
                "ROI",
                "Value",
                "Raw Text",
                "Confidence",
                "Reading ID",
            ]
        )

        layout = QVBoxLayout()

        layout.addWidget(self.table)

        self.setLayout(layout)

    def update_reading(
        self,
        reading_id: int,
        roi_name: str,
        value,
        raw_text: str,
        confidence: float,
    ) -> None:
        """
        Adds latest OCR reading to table.
        """

        row = self.table.rowCount()

        self.table.insertRow(row)

        self.table.setItem(row, 0, QTableWidgetItem(roi_name))
        self.table.setItem(row, 1, QTableWidgetItem(str(value)))
        self.table.setItem(row, 2, QTableWidgetItem(raw_text))
        self.table.setItem(row, 3, QTableWidgetItem(f"{confidence:.2f}"))
        self.table.setItem(row, 4, QTableWidgetItem(str(reading_id)))

        self.table.resizeColumnsToContents()

    def clear(self) -> None:
        """
        Clears current readings table.
        """

        self.table.setRowCount(0)