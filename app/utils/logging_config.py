import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


def setup_logging():
    logger = logging.getLogger()

    if logger.handlers:
        return

    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(
        os.path.join(LOG_DIR, "app.log"),
        maxBytes=5_000_000,
        backupCount=3,
    )

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)
