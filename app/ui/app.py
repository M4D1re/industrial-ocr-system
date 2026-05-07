import sys

from PySide6.QtWidgets import QApplication


class IndustrialApplication(QApplication):
    """
    Main Qt application.
    """

    def __init__(self) -> None:
        super().__init__(sys.argv)