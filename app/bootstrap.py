from app.config.config_manager import ConfigManager
from app.ui.app import IndustrialApplication
from app.ui.themes import DARK_THEME
from app.ui.windows.main_window import MainWindow
from app.utils.logger import setup_logger
from app.utils.paths import ensure_directories


class Bootstrap:
    """
    Application bootstrapper.
    """

    def __init__(self) -> None:
        ensure_directories()

        self.logger = setup_logger()

        self.config_manager = ConfigManager()

        self.config = self.config_manager.load()

        self.logger.info("Configuration loaded")

        self.app = IndustrialApplication()

        self.app.setStyleSheet(DARK_THEME)

        self.main_window = MainWindow()

    def run(self) -> int:
        """
        Starts application.
        """

        self.main_window.show()

        self.logger.info("Main window displayed")

        return self.app.exec()