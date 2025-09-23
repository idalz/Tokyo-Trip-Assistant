"""
Logging configuration for Tokyo Trip Assistant.
Provides structured logging with different levels for different environments.
"""

import logging
import sys
from datetime import datetime
from typing import Optional

from .config import settings


class ColoredFormatter(logging.Formatter):
    """Colored log formatter for development."""

    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }

    def format(self, record):
        if settings.DEBUG:
            color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
            record.levelname = f"{color}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)


def setup_logging() -> logging.Logger:
    """Setup application logging."""

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)

    if settings.DEBUG:
        # Detailed format for development
        formatter = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    else:
        # JSON-like format for production
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "logger": "%(name)s", '
            '"level": "%(levelname)s", "message": "%(message)s"}'
        )

    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Application logger
    app_logger = logging.getLogger("tokyo_trip_assistant")

    return app_logger


# Global logger instance
logger = setup_logging()