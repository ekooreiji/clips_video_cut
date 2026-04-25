"""
Common Exceptions - Exceções customizadas do sistema
"""

from src.common.exceptions.base import (
    BaseException,
    VideoException,
    VideoNotFoundError,
    VideoCorruptedError,
    ProcessingException,
    FFmpegNotFoundError,
    WhisperError,
    ConfigurationError,
)

__all__ = [
    "BaseException",
    "VideoException",
    "VideoNotFoundError",
    "VideoCorruptedError", 
    "ProcessingException",
    "FFmpegNotFoundError",
    "WhisperError",
    "ConfigurationError",
]