import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from src.config import PATHS, config


def setup_logging() -> logging.Logger:
    log_dir = PATHS["logs"]
    log_file = config["logging"]["file"]
    log_level = config["logging"]["level"]
    max_bytes = config["logging"]["max_bytes"]
    backup_count = config["logging"]["backup_count"]
    enable_console = config["logging"]["enable_console"]

    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = Path(log_dir) / log_file

    logger = logging.getLogger("email_automation")
    logger.setLevel(getattr(logging, log_level, logging.INFO))
    logger.handlers.clear()
    logger.propagate = False

    formatter = logging.Formatter("%(message)s")

    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if enable_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
