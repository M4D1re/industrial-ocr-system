import json
from pathlib import Path

from app.config.settings import AppConfig
from app.utils.paths import CONFIG_DIR


class ConfigManager:
    """
    Application configuration manager.
    """

    CONFIG_FILE = CONFIG_DIR / "settings.json"

    def __init__(self) -> None:
        self.config = AppConfig()

    def load(self) -> AppConfig:
        """
        Loads configuration from disk.
        """

        if not self.CONFIG_FILE.exists():
            self.save()
            return self.config

        with open(self.CONFIG_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.config = AppConfig(**data)

        return self.config

    def save(self) -> None:
        """
        Saves configuration to disk.
        """

        with open(self.CONFIG_FILE, "w", encoding="utf-8") as file:
            json.dump(
                self.config.model_dump(),
                file,
                indent=4,
            )