"""
Video Exceptions - Exceções relacionadas a vídeos
"""

from src.common.exceptions.base import VideoException


class VideoProcessingError(VideoException):
    """Exceção base para erros no processamento de vídeo."""

    def __init__(self, message: str, path: str = None):
        self.path = path
        details = f"Arquivo: {path}" if path else None
        super().__init__(message, details)


class VideoNotFoundError(VideoProcessingError):
    """Exceção para quando o vídeo não é encontrado."""

    def __init__(self, path: str):
        super().__init__("Vídeo não encontrado no caminho especificado", path)


class VideoCorruptedError(VideoProcessingError):
    """Exceção para quando o vídeo está corrompido ou ilegível."""

    def __init__(self, path: str):
        super().__init__("Vídeo corrompido ou não suportado", path)


class VideoFormatError(VideoProcessingError):
    """Exceção para formato de vídeo não suportado."""

    def __init__(self, path: str, format: str):
        self.format = format
        super().__init__(
            f"Formato não suportado: {format}",
            path
        )


class VideoNoAudioError(VideoProcessingError):
    """Exceção para quando o vídeo não tem áudio."""

    def __init__(self, path: str):
        super().__init__("Vídeo não contém faixa de áudio", path)