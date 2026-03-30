"""
Logging Configuration
"""

import logging
import os
from app.utils.config import settings


def setup_logging() -> logging.Logger:
    """Set up application logging"""
    
    # Create logger
    logger = logging.getLogger("gt3r_diagnostic")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler (if log file is specified)
    if settings.LOG_FILE:
        try:
            os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)
            file_handler = logging.FileHandler(settings.LOG_FILE)
            file_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Could not set up file logging: {e}")
    
    return logger


# Create global logger instance
logger = setup_logging()