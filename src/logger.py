import logging
from pathlib import Path
import sys
from datetime import datetime


class ExperimentLogger:
    """Handles logging configuration for experiments."""

    def __init__(
        self, logger_name: str, log_dir: str = "logs", level: int = logging.INFO
    ):
        """
        Initialize logger with given name and configuration.

        Args:
            logger_name: Name of the logger
            log_dir: Directory to store log files
            level: Logging level
        """
        self.logger_name = logger_name
        self.log_dir = Path(log_dir)
        self.level = level

        # Create logs directory if it doesn't exist
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Initialize logger
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Configure and return a logger with file and console handlers."""
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.level)

        # Clear existing handlers
        if logger.hasHandlers():
            logger.handlers.clear()

        # Add handlers
        logger.addHandler(self._get_file_handler())
        logger.addHandler(self._get_console_handler())

        return logger

    def _get_file_handler(self) -> logging.FileHandler:
        """Create a file handler for the logger."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.log_dir / f"{self.logger_name}_{timestamp}.log"

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(self.level)
        file_handler.setFormatter(self._get_formatter(detailed=True))

        return file_handler

    def _get_console_handler(self) -> logging.StreamHandler:
        """Create a console handler for the logger."""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.level)
        console_handler.setFormatter(self._get_formatter(detailed=False))

        return console_handler

    def _get_formatter(self, detailed: bool = True) -> logging.Formatter:
        """Get formatter for log messages."""
        if detailed:
            format_str = (
                f"[{self.logger_name}] %(asctime)s - %(levelname)s - "
                "%(filename)s:%(lineno)d - %(message)s"
            )
        else:
            format_str = f"[{self.logger_name}] %(levelname)s - %(message)s"

        formatter = logging.Formatter(format_str)
        formatter.datefmt = "%Y-%m-%d %H:%M:%S"

        return formatter

    def get_logger(self) -> logging.Logger:
        """Return the configured logger."""
        return self.logger


# Usage example:
def get_experiment_logger(experiment_name: str) -> logging.Logger:
    """Get a logger for a specific experiment."""
    logger_manager = ExperimentLogger(
        logger_name=experiment_name, log_dir="logs/experiments", level=logging.INFO
    )
    return logger_manager.get_logger()
