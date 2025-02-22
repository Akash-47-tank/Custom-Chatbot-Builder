"""Logging utility for the chatbot builder."""

import sys
from pathlib import Path
from typing import Optional

from loguru import logger

from ..config.config import LOGGING_CONFIG


def setup_logger(log_file: Optional[Path] = None) -> None:
    """
    Set up the logger with the specified configuration.

    Args:
        log_file (Optional[Path]): Path to the log file. If None, uses the default from config.

    Returns:
        None
    """
    try:
        # Remove any existing handlers
        logger.remove()

        # Add console handler
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level=LOGGING_CONFIG["level"],
        )

        # Add file handler
        log_path = log_file or LOGGING_CONFIG["log_file"]
        logger.add(
            log_path,
            rotation=LOGGING_CONFIG["rotation"],
            retention=LOGGING_CONFIG["retention"],
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level=LOGGING_CONFIG["level"],
        )

        logger.info(f"Logger initialized. Log file: {log_path}")
    except Exception as e:
        print(f"Error setting up logger: {str(e)}")
        raise


def get_logger():
    """
    Get the configured logger instance.

    Returns:
        Logger: Configured logger instance
    """
    return logger
