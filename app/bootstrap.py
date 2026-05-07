from app.config.config_manager import ConfigManager
from app.ui.app import IndustrialApplication
from app.ui.themes import DARK_THEME
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

        self.logger.info("Application configuration loaded")

        self.app = IndustrialApplication()

        self.app.setStyleSheet(DARK_THEME)

    def run(self) -> int:
        """
        Starts application event loop.
        """

        self.logger.info("Starting application")

        return self.app.exec()