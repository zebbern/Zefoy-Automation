"""
Logging configuration for Zefoy Automation Bot
Provides structured logging to both console and file
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional
from colorama import Fore, Style, init

from src import config

# Initialize colorama
init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to console output"""
    
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        # Add color to levelname
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{Style.RESET_ALL}"
        return super().format(record)


class BotLogger:
    """
    Centralized logging system for the bot
    Supports both file and console logging with different formats
    """
    
    _instance: Optional['BotLogger'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._logger is not None:
            return
        
        self._logger = logging.getLogger(config.APP_NAME)
        self._logger.setLevel(logging.DEBUG)
        self._logger.handlers.clear()
        
        # File Handler - Detailed logging
        file_handler = RotatingFileHandler(
            config.LOG_FILE,
            maxBytes=config.LOG_MAX_BYTES,
            backupCount=config.LOG_BACKUP_COUNT,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(config.LOG_FORMAT)
        file_handler.setFormatter(file_formatter)
        self._logger.addHandler(file_handler)
        
        # Console Handler - User-friendly output
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = ColoredFormatter('%(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        self._logger.addHandler(console_handler)
    
    @property
    def logger(self) -> logging.Logger:
        """Get the logger instance"""
        return self._logger
    
    def debug(self, message: str, *args, **kwargs):
        """Log debug message"""
        self._logger.debug(message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs):
        """Log info message"""
        self._logger.info(message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs):
        """Log warning message"""
        self._logger.warning(message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs):
        """Log error message"""
        self._logger.error(message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs):
        """Log critical message"""
        self._logger.critical(message, *args, **kwargs)
    
    def exception(self, message: str, *args, **kwargs):
        """Log exception with traceback"""
        self._logger.exception(message, *args, **kwargs)


# Global logger instance
_bot_logger = BotLogger()


def get_logger() -> BotLogger:
    """Get the global logger instance"""
    return _bot_logger


# Convenience functions
def debug(message: str, *args, **kwargs):
    """Log debug message"""
    _bot_logger.debug(message, *args, **kwargs)


def info(message: str, *args, **kwargs):
    """Log info message"""
    _bot_logger.info(message, *args, **kwargs)


def warning(message: str, *args, **kwargs):
    """Log warning message"""
    _bot_logger.warning(message, *args, **kwargs)


def error(message: str, *args, **kwargs):
    """Log error message"""
    _bot_logger.error(message, *args, **kwargs)


def critical(message: str, *args, **kwargs):
    """Log critical message"""
    _bot_logger.critical(message, *args, **kwargs)


def exception(message: str, *args, **kwargs):
    """Log exception with traceback"""
    _bot_logger.exception(message, *args, **kwargs)
