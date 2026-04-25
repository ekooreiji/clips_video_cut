"""
Value Object Configuration

Configurações de processamento para o sistema.
"""

from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum
import json
from pathlib import Path


class Sensitivity(Enum):
    """Níveis de sensibilidade para detecção"""
    LOW = 0.3
    MEDIUM = 1.0
    HIGH = 2.0


@dataclass
class VisualCutConfig:
    """Configuração para corte visual"""
    enabled: bool = True
    sensitivity: float = 1.0  # MEDIUM padrão
    sample_rate: int = 5  # analisa a cada N frames


@dataclass
class SilenceConfig:
    """Configuração para remoção de silêncio"""
    enabled: bool = False
    db_threshold: int = -40  # dB
    min_duration: float = 0.5  # segundos


@dataclass
class NormalizationConfig:
    """Configuração para normalização de áudio"""
    enabled: bool = False


@dataclass
class SubtitlesConfig:
    """Configuração para legendas"""
    enabled: bool = False
    format: str = "srt"  # srt ou vtt
    burn: bool = False  # inserir no vídeo
    whisper_model: str = "base"  # modelo Whisper


@dataclass
class OutputConfig:
    """Configuração de saída"""
    format: str = "same"  # same, mp4, mkv
    quality: str = "original"  # original, high, medium, low
    keep_original: bool = True
    max_workers: int = 3


@dataclass
class LoggingConfig:
    """Configuração de logging"""
    level: str = "INFO"
    file: str = "app.log"


@dataclass
class ProcessingConfig:
    """
    Configuração principal de processamento.
    
    Attributes:
        visual_cut: Configuração para corte visual
        silence: Configuração para silêncio
        normalization: Configuração para normalização
        subtitles: Configuração para legendas
        output: Configuração de saída
        logging: Configuração de logging
    """
    visual_cut: VisualCutConfig = field(default_factory=VisualCutConfig)
    silence: SilenceConfig = field(default_factory=SilenceConfig)
    normalization: NormalizationConfig = field(default_factory=NormalizationConfig)
    subtitles: SubtitlesConfig = field(default_factory=SubtitlesConfig)
    output: OutputConfig = field(default_factory=OutputConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    
    @staticmethod
    def from_json(path: Path) -> "ProcessingConfig":
        """Carrega configuração de arquivo JSON"""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        config = ProcessingConfig()
        
        # Visual Cut
        if 'processing' in data and 'visual_cut' in data['processing']:
            vc = data['processing']['visual_cut']
            config.visual_cut = VisualCutConfig(
                enabled=vc.get('enabled', True),
                sensitivity=vc.get('sensitivity', 1.0),
                sample_rate=vc.get('sample_rate', 5)
            )
        
        # Silence
        if 'processing' in data and 'silence_removal' in data['processing']:
            sc = data['processing']['silence_removal']
            config.silence = SilenceConfig(
                enabled=sc.get('enabled', False),
                db_threshold=sc.get('db_threshold', -40),
                min_duration=sc.get('min_duration', 0.5)
            )
        
        # Normalization
        if 'processing' in data and 'normalization' in data['processing']:
            config.normalization = NormalizationConfig(
                enabled=data['processing']['normalization'].get('enabled', False)
            )
        
        # Subtitles
        if 'subtitles' in data:
            config.subtitles = SubtitlesConfig(
                enabled=data['subtitles'].get('enabled', False),
                format=data['subtitles'].get('format', 'srt'),
                burn=data['subtitles'].get('burn', False),
                whisper_model=data['subtitles'].get('whisper_model', 'base')
            )
        
        # Output
        if 'output' in data:
            config.output = OutputConfig(
                format=data['output'].get('format', 'same'),
                quality=data['output'].get('quality', 'original'),
                keep_original=data['output'].get('keep_original', True),
                max_workers=data['output'].get('max_workers', 3)
            )
        
        # Logging
        if 'logging' in data:
            config.logging = LoggingConfig(
                level=data['logging'].get('level', 'INFO'),
                file=data['logging'].get('file', 'app.log')
            )
        
        return config
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            "processing": {
                "visual_cut": {
                    "enabled": self.visual_cut.enabled,
                    "sensitivity": self.visual_cut.sensitivity,
                    "sample_rate": self.visual_cut.sample_rate
                },
                "silence_removal": {
                    "enabled": self.silence.enabled,
                    "db_threshold": self.silence.db_threshold,
                    "min_duration": self.silence.min_duration
                },
                "normalization": {
                    "enabled": self.normalization.enabled
                }
            },
            "subtitles": {
                "enabled": self.subtitles.enabled,
                "format": self.subtitles.format,
                "burn": self.subtitles.burn,
                "whisper_model": self.subtitles.whisper_model
            },
            "output": {
                "format": self.output.format,
                "quality": self.output.quality,
                "keep_original": self.output.keep_original,
                "max_workers": self.output.max_workers
            },
            "logging": {
                "level": self.logging.level,
                "file": self.logging.file
            }
        }
    
    def save_json(self, path: Path):
        """Salva configuração em arquivo JSON"""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2)