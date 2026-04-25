"""
Value Object Timestamp

Representa um timestamp com precisão para vídeos.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Timestamp:
    """
    Value object representando um timestamp em segundos.
    
    Attributes:
        seconds: Tempo em segundos com precisão de milissegundos
    """
    seconds: float
    
    @property
    def milliseconds(self) -> int:
        """Retorna o tempo em milissegundos"""
        return int(self.seconds * 1000)
    
    @property
    def formatted(self) -> str:
        """Retorna no formato HH:MM:SS.mmm"""
        hours = int(self.seconds // 3600)
        minutes = int((self.seconds % 3600) // 60)
        secs = self.seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"
    
    @property
    def srt_format(self) -> str:
        """Retorna no formato SRT HH:MM:SS,mmm"""
        hours = int(self.seconds // 3600)
        minutes = int((self.seconds % 3600) // 60)
        secs = self.seconds % 60
        millis = int((secs - int(secs)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{int(secs):02d},{millis:03d}"
    
    @property
    def vtt_format(self) -> str:
        """Retorna no formato VTT HH:MM:SS.mmm"""
        hours = int(self.seconds // 3600)
        minutes = int((self.seconds % 3600) // 60)
        secs = self.seconds % 60
        millis = int((secs - int(secs)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{int(secs):02d}.{millis:03d}"
    
    @staticmethod
    def from_frame(frame: int, fps: float) -> "Timestamp":
        """Cria timestamp a partir de frame e FPS"""
        return Timestamp(seconds=frame / fps)
    
    @staticmethod
    def from_srt(time_str: str) -> "Timestamp":
        """Cria timestamp a partir de string SRT"""
        # Formato: HH:MM:SS,mmm
        time_str = time_str.replace(',', '.')
        parts = time_str.split(':')
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = float(parts[2])
        return Timestamp(seconds=hours * 3600 + minutes * 60 + seconds)
    
    def to_tuple(self) -> Tuple[int, int, int, int]:
        """Retorna como (hours, minutes, seconds, milliseconds)"""
        hours = int(self.seconds // 3600)
        minutes = int((self.seconds % 3600) // 60)
        secs = int(self.seconds % 60)
        millis = int((self.seconds - int(self.seconds)) * 1000)
        return (hours, minutes, secs, millis)
    
    def __str__(self) -> str:
        return self.formatted
    
    def __repr__(self) -> str:
        return f"Timestamp({self.seconds:.3f})"
    
    def __add__(self, other: "Timestamp") -> "Timestamp":
        return Timestamp(seconds=self.seconds + other.seconds)
    
    def __sub__(self, other: "Timestamp") -> "Timestamp":
        return Timestamp(seconds=max(0, self.seconds - other.seconds))
    
    def __mul__(self, factor: float) -> "Timestamp":
        return Timestamp(seconds=self.seconds * factor)
    
    def __eq__(self, other: "Timestamp") -> bool:
        return abs(self.seconds - other.seconds) < 0.001
    
    def __lt__(self, other: "Timestamp") -> bool:
        return self.seconds < other.seconds