"""
Processing Exceptions - Exceções relacionadas ao processamento
"""

from src.common.exceptions.base import ProcessingException


class FFmpegNotFoundError(ProcessingException):
    """Exceção para quando FFmpeg não está instalado."""

    def __init__(self):
        super().__init__(
            "FFmpeg não encontrado no sistema",
            "Instale o FFmpeg e certifique-se que está no PATH"
        )


class WhisperError(ProcessingException):
    """Exceção para erros do Whisper."""

    def __init__(self, message: str, details: str = None):
        super().__init__(f"Erro no Whisper: {message}", details)


class SubtitleGenerationError(ProcessingException):
    """Exceção para erros de geração de legendas."""

    def __init__(self, message: str, video_path: str = None):
        self.video_path = video_path
        super().__init__(message, video_path)


class VideoCutError(ProcessingException):
    """Exceção para erros ao cortar vídeo."""

    def __init__(self, message: str, video_path: str = None):
        super().__init__(message, video_path)


class AudioProcessingError(ProcessingException):
    """Exceção para erros de processamento de áudio."""

    def __init__(self, message: str, video_path: str = None):
        super().__init__(message, video_path)