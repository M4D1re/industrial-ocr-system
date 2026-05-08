import time

import cv2

from PySide6.QtCore import QThread, Signal


class CameraService(QThread):
    """
    Camera worker thread.
    """

    frame_ready = Signal(object)

    connection_changed = Signal(bool)

    fps_updated = Signal(float)

    def __init__(self, source: str) -> None:
        super().__init__()

        self.source = source

        self.running = False

        self.capture = None

    def run(self) -> None:
        """
        Main camera loop.
        """

        self.running = True

        source = int(self.source) if self.source.isdigit() else self.source

        self.capture = cv2.VideoCapture(source)

        if not self.capture.isOpened():
            self.connection_changed.emit(False)
            return

        self.connection_changed.emit(True)

        previous_time = time.time()

        while self.running:
            success, frame = self.capture.read()

            if not success:
                continue

            current_time = time.time()

            fps = 1 / (current_time - previous_time)

            previous_time = current_time

            self.fps_updated.emit(fps)

            self.frame_ready.emit(frame)

        self.capture.release()

    def stop(self) -> None:
        """
        Stops camera thread.
        """

        self.running = False

        self.wait()