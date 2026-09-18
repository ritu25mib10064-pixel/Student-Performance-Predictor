"""
logger.py
---------
Provides a single, reusable logger for the whole project.
Satisfies the Logging/Monitoring non-functional requirement.
"""

import logging
from src.config import LOG_PATH


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger that writes to both console and a log file."""
    logger = logging.getLogger(name)

    if not logger.handlers:  # avoid duplicate handlers on repeated calls
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        try:
            file_handler = logging.FileHandler(LOG_PATH)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except OSError:
            # If the log file cannot be created (e.g., read-only FS), fall
            # back silently to console-only logging rather than crashing.
            pass

    return logger
