"""
Entidade ClipSegment

Representa um segmento de clip com timestamps de início e fim.
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class ClipReason(Enum):
    """Motivo da criação do clip"""
    SCENE_CHANGE = "scene_change"
    SILENCE_REMOVAL = "silence_removal"
    MANUAL = "manual"
    CUSTOM_JSON = "custom_json"


@dataclass
class ClipSegment:
    """
    Entidade que representa um segmento de clip extraído do vídeo.
    
    Attributes:
        id: Identificador único do clip
        start_time: Tempo de início em segundos
        end_time: Tempo de fim em segundos
        reason: Motivo da criação do clip
        scene_score: Score de detecção (opcional)
    """
    id: int
    start_time: float
    end_time: float
    reason: ClipReason = ClipReason.SCENE_CHANGE
    scene_score: Optional[float] = None
    
    def __post_init__(self):
        """Valida os dados após inicialização"""
        # Validar timestamps
        if self.start_time < 0:
            raise ValueError(f"start_time não pode ser negativo: {self.start_time}")
        
        if self.end_time < 0:
            raise ValueError(f"end_time não pode ser negativo: {self.end_time}")
        
        if self.end_time < self.start_time:
            raise ValueError(
                f"end_time ({self.end_time}) não pode ser menor que "
                f"start_time ({self.start_time})"
            )
        
        # Validar ID
        if self.id < 0:
            raise ValueError(f"id não pode ser negativo: {self.id}")
    
    @property
    def duration(self) -> float:
        """Duração do clip em segundos"""
        return self.end_time - self.start_time
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            "id": self.id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration,
            "reason": self.reason.value
        }
    
    def __str__(self) -> str:
        return f"ClipSegment({self.id}: {self.start_time:.2f}s - {self.end_time:.2f}s)"
    
    def __repr__(self) -> str:
        return f"ClipSegment(id={self.id}, start={self.start_time}, end={self.end_time}, reason={self.reason.value})"