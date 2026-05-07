from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent.parent

APP_DIR = ROOT_DIR / "app"
CONFIG_DIR = ROOT_DIR / "config"
DATA_DIR = ROOT_DIR / "data"
LOGS_DIR = ROOT_DIR / "logs"

DATABASE_PATH = DATA_DIR / "app.db"


def ensure_directories() -> None:
    """
    Creates required project directories if they do not exist.
    """

    directories = [
        CONFIG_DIR,
        DATA_DIR,
        LOGS_DIR,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)