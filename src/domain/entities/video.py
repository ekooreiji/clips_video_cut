"""
Entidade VideoDocument

Representa um documento de vídeo com seus metadados e informações.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from datetime import datetime


@dataclass
class VideoMetadata:
    """Metadados do vídeo"""
    width: int
    height: int
    fps: float
    codec: str
    bitrate: Optional[int] = None
    duration: float = 0.0
    has_audio: bool = True
    audio_codec: Optional[str] = None
    audio_channels: int = 0
    audio_sample_rate: int = 0


@dataclass
class VideoDocument:
    """
    Entidade que representa um documento de vídeo.
    
    Attributes:
        path: Caminho absoluto do arquivo de vídeo
        metadata: Metadados do vídeo (lidos automaticamente)
        created_at: Data de criação do documento
    """
    path: Path
    metadata: Optional[VideoMetadata] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Converte path para Path se for string"""
        if isinstance(self.path, str):
            self.path = Path(self.path)
    
    @property
    def name(self) -> str:
        """Retorna o nome do arquivo sem extensão"""
        return self.path.stem
    
    @property
    def extension(self) -> str:
        """Retorna a extensão do arquivo"""
        return self.path.suffix.lower()
    
    @property
    def directory(self) -> Path:
        """Retorna o diretório do arquivo"""
        return self.path.parent
    
    @property
    def output_directory(self) -> Path:
        """Retorna o diretório de saída para clips"""
        return self.directory / "clips"
    
    def exists(self) -> bool:
        """Verifica se o arquivo existe"""
        return self.path.exists()
    
    def is_valid_format(self) -> bool:
        """Verifica se o formato é suportado"""
        valid_extensions = {'.mp4', '.mkv', '.avi', '.webm', '.mov'}
        return self.extension in valid_extensions
    
    def __str__(self) -> str:
        return f"VideoDocument(path={self.path.name})"
    
    def __repr__(self) -> str:
        return f"VideoDocument(path='{self.path}', metadata={self.metadata})"