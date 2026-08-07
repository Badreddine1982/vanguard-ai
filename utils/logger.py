import os
import sys
from pathlib import Path

from loguru import logger


def setup_logging():
    """تهيئة نظام التسجيل الموحد"""
    logger.remove()

    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>",
        colorize=True,
        level="INFO",
    )

    logs_dir = Path(os.getenv("VANGUARD_LOGS_DIR", "./logs"))
    logs_dir.mkdir(parents=True, exist_ok=True)

    logger.add(
        logs_dir / "vanguard_{time:YYYY-MM-DD}.log",
        rotation="10 MB",
        retention="5 days",
        compression="zip",
        format="{time} | {level} | {name} - {message}",
        level="DEBUG",
    )

    return logger


__all__ = ["logger", "setup_logging"]
