import numpy as np
from PySide6.QtCore import QPoint, QRect, Qt, Signal
from PySide6.QtGui import QImage, QMouseEvent, QPainter, QPen
from PySide6.QtWidgets import QWidget

from app.models.roi_model import ROIModel

from PySide6.QtCore import QPoint, QRect, Qt, Signal





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

        self.placeholder_text = "Активные камеры отсутствуют"

        self.last_cv_frame: np.ndarray | None = None

        self.roi_regions: list[ROIModel] = []

        self.drawing = False

        self.start_point: QPoint | None = None

        self.current_rect: QRect | None = None

        self.setMinimumSize(800, 600)

    def update_cv_frame(self, frame: np.ndarray) -> None:
        """
        Stores latest OpenCV frame for OCR processing.
        """

        self.last_cv_frame = frame.copy()

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
                self.placeholder_text,
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

        frame_rect = self._widget_rect_to_frame_rect(self.current_rect)

        if frame_rect is None:
            self.current_rect = None
            self.update()
            return

        roi = ROIModel(
            id=roi_id,
            name=f"ROI {roi_id}",
            x=frame_rect.x(),
            y=frame_rect.y(),
            width=frame_rect.width(),
            height=frame_rect.height(),
        )

        self.roi_regions.append(roi)

        self.roi_created.emit(roi)

        self.current_rect = None

        self.update()

    def _draw_roi_regions(self, painter: QPainter) -> None:
        """
        Draws saved ROI rectangles.
        """

        for roi in self.roi_regions:
            if roi.enabled:
                pen = QPen(Qt.green)
            else:
                pen = QPen(Qt.gray)

            pen.setWidth(2)
            painter.setPen(pen)

            rect = self._frame_rect_to_widget_rect(
                QRect(
                    roi.x,
                    roi.y,
                    roi.width,
                    roi.height,
                )
            )

            if rect is None:
                continue

            painter.drawRect(rect)

            painter.drawText(
                rect.topLeft() + QPoint(4, -4),
                f"{roi.name} {'ON' if roi.enabled else 'OFF'}",
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

    def _get_video_display_rect(self) -> QRect | None:
        """
        Returns actual video rectangle inside widget.
        """

        if self.current_frame is None:
            return None

        scaled = self.current_frame.scaled(
            self.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )

        x = (self.width() - scaled.width()) // 2
        y = (self.height() - scaled.height()) // 2

        return QRect(x, y, scaled.width(), scaled.height())

    def _widget_rect_to_frame_rect(self, rect: QRect) -> QRect | None:
        """
        Converts widget coordinates to original camera frame coordinates.
        """

        if self.current_frame is None:
            return None

        video_rect = self._get_video_display_rect()

        if video_rect is None:
            return None

        intersected = rect.intersected(video_rect)

        if intersected.isEmpty():
            return None

        scale_x = self.current_frame.width() / video_rect.width()
        scale_y = self.current_frame.height() / video_rect.height()

        x = int((intersected.x() - video_rect.x()) * scale_x)
        y = int((intersected.y() - video_rect.y()) * scale_y)
        width = int(intersected.width() * scale_x)
        height = int(intersected.height() * scale_y)

        return QRect(x, y, width, height)

    def _frame_rect_to_widget_rect(self, rect: QRect) -> QRect | None:
        """
        Converts original camera frame coordinates to widget coordinates.
        """

        if self.current_frame is None:
            return None

        video_rect = self._get_video_display_rect()

        if video_rect is None:
            return None

        scale_x = video_rect.width() / self.current_frame.width()
        scale_y = video_rect.height() / self.current_frame.height()

        x = int(video_rect.x() + rect.x() * scale_x)
        y = int(video_rect.y() + rect.y() * scale_y)
        width = int(rect.width() * scale_x)
        height = int(rect.height() * scale_y)

        return QRect(x, y, width, height)

    def clear_roi_regions(self) -> None:
        """
        Clears all ROI regions from video widget.
        """

        self.roi_regions.clear()

        self.update()

    def set_placeholder_text(self, text: str) -> None:
        """
        Sets placeholder text shown when no video frame is available.
        """

        self.placeholder_text = text

        self.current_frame = None
        self.last_cv_frame = None

        self.update()