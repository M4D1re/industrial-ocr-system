from PySide6.QtCore import QPoint, QRect, Qt, Signal
from PySide6.QtGui import QImage, QMouseEvent, QPainter, QPen
from PySide6.QtWidgets import QWidget

from app.models.roi_model import ROIModel



class VideoWidget(QWidget):
    """
    Live video display widget with ROI overlay editor.
    """

    roi_created = Signal(object)
    roi_deleted = Signal(object)

    MAX_ROI_COUNT = 10

    def __init__(self) -> None:
        super().__init__()

        self.current_frame: QImage | None = None

        self.roi_regions: list[ROIModel] = []

        self.drawing = False

        self.start_point: QPoint | None = None

        self.current_rect: QRect | None = None

        self.setMinimumSize(800, 600)

    def update_frame(self, image: QImage) -> None:
        """
        Updates displayed frame.
        """

        self.current_frame = image

        self.update()

    def paintEvent(self, event) -> None:
        """
        Renders video frame and ROI overlays.
        """

        painter = QPainter(self)

        painter.fillRect(self.rect(), Qt.black)

        if self.current_frame:
            scaled = self.current_frame.scaled(
                self.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )

            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2

            painter.drawImage(x, y, scaled)

        else:
            painter.setPen(Qt.white)
            painter.drawText(
                self.rect(),
                Qt.AlignCenter,
                "NO VIDEO SIGNAL",
            )

        self._draw_roi_regions(painter)

        if self.current_rect:
            pen = QPen(Qt.yellow)
            pen.setWidth(2)
            painter.setPen(pen)
            painter.drawRect(self.current_rect)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Starts ROI drawing.
        """

        if event.button() != Qt.LeftButton:
            return

        if len(self.roi_regions) >= self.MAX_ROI_COUNT:
            return

        self.drawing = True

        self.start_point = event.position().toPoint()

        self.current_rect = QRect(self.start_point, self.start_point)

        self.update()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """
        Updates ROI rectangle while mouse is moving.
        """

        if not self.drawing or self.start_point is None:
            return

        current_point = event.position().toPoint()

        self.current_rect = QRect(
            self.start_point,
            current_point,
        ).normalized()

        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """
        Finishes ROI drawing.
        """

        if event.button() != Qt.LeftButton:
            return

        if not self.drawing or self.current_rect is None:
            return

        self.drawing = False

        if self.current_rect.width() < 10 or self.current_rect.height() < 10:
            self.current_rect = None
            self.update()
            return

        roi_id = len(self.roi_regions) + 1

        roi = ROIModel(
            id=roi_id,
            name=f"ROI {roi_id}",
            x=self.current_rect.x(),
            y=self.current_rect.y(),
            width=self.current_rect.width(),
            height=self.current_rect.height(),
        )

        self.roi_regions.append(roi)

        self.roi_created.emit(roi)

        self.current_rect = None

        self.update()

    def _draw_roi_regions(self, painter: QPainter) -> None:
        """
        Draws saved ROI rectangles.
        """

        pen = QPen(Qt.green)
        pen.setWidth(2)
        painter.setPen(pen)

        for roi in self.roi_regions:
            rect = QRect(
                roi.x,
                roi.y,
                roi.width,
                roi.height,
            )

            painter.drawRect(rect)

            painter.drawText(
                rect.topLeft() + QPoint(4, -4),
                roi.name,
            )

    def delete_roi(self, roi_id: int) -> None:
        """
        Deletes ROI by id.
        """

        self.roi_regions = [
            roi for roi in self.roi_regions if roi.id != roi_id
        ]

        self.roi_deleted.emit(roi_id)

        self.update()

    def set_roi_regions(self, roi_regions: list[ROIModel]) -> None:
        """
        Loads ROI regions into video widget.
        """

        self.roi_regions = roi_regions

        self.update()