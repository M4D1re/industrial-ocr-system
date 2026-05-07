import logging
from logging.handlers import RotatingFileHandler

from app.utils.paths import LOGS_DIR


def setup_logger() -> logging.Logger:
    """
    Configures production logger.
    """

    logger = logging.getLogger("industrial_ocr")

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    log_file = LOGS_DIR / "application.log"

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger