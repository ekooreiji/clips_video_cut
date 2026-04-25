"""
Base Exceptions - Exceções base do sistema
"""


class BaseException(Exception):
    """Exceção base para o sistema"""
    
    def __init__(self, message: str, details: str = None):
        self.message = message
        self.details = details
        super().__init__(self.message)
    
    def __str__(self) -> str:
        if self.details:
            return f"{self.message}: {self.details}"
        return self.message


class VideoException(BaseException):
    """Exceção base para erros de vídeo"""
    pass


class ProcessingException(BaseException):
    """Exceção base para erros de processamento"""
    pass


class ConfigurationException(BaseException):
    """Exceção base para erros de configuração"""
    pass


class VideoNotFoundError(VideoException):
    """Exceção para quando o vídeo não é encontrado"""
    def __init__(self, path: str):
        super().__init__(f"Vídeo não encontrado: {path}", path)


class VideoCorruptedError(VideoException):
    """Exceção para quando o vídeo está corrompido"""
    def __init__(self, path: str):
        super().__init__(f"Vídeo corrompido ou não suportado: {path}", path)


class FFmpegNotFoundError(ProcessingException):
    """Exceção para quando FFmpeg não está instalado"""
    def __init__(self):
        super().__init__(
            "FFmpeg não encontrado no sistema",
            "Instale o FFmpeg e adicione ao PATH"
        )


class WhisperError(ProcessingException):
    """Exceção para erros do Whisper"""
    def __init__(self, message: str, details: str = None):
        super().__init__(f"Erro no Whisper: {message}", details)


class ConfigurationError(ConfigurationException):
    """Exceção para erros de configuração"""
    def __init__(self, message: str, details: str = None):
        super().__init__(message, details)