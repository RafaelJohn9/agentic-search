"""
Module for setting up and configuring logging in a Python application.

This module provides a function to create a logger with multiple handlers,
including console, file, and memory handlers. It also includes a function
to retrieve the contents of the in-memory log buffer.
"""

import logging
import io

_log_buffer = io.StringIO()


def setup_logger(name: str = "app_logger") -> logging.Logger:
    """
    Set up and configure a logger with specified handlers and formatting.

    This function creates a logger with the given name, sets its logging level to
    INFO, and attaches three handlers: a console handler, a file handler, and a
    memory handler. Each handler is configured with a consistent log message
    format. If the logger already has handlers, no additional handlers are added.

    Args:
        name (str): The name of the logger. Defaults to "app_logger".

    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.hasHandlers():
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # Handlers
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler("app.log")
        memory_handler = logging.StreamHandler(_log_buffer)

        for handler in (console_handler, file_handler, memory_handler):
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        logger.propagate = False

    return logger


def get_log_buffer() -> str:
    """Retrieve the contents of the in-memory log buffer."""
    return _log_buffer.getvalue()
