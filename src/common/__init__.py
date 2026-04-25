"""
Common - Componentes compartilhados do sistema
"""

from src.common.exceptions import (
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