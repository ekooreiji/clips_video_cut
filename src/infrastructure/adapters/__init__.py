"""
Infrastructure Adapters - Adapters de Infraestrutura
"""

from src.infrastructure.adapters.ffmpeg_adapter import FFmpegAdapter
from src.infrastructure.adapters.opencv_adapter import OpenCVAdapter
from src.infrastructure.adapters.audio_adapter import AudioAdapter
from src.infrastructure.adapters.whisper_adapter import WhisperAdapter

__all__ = [
    "FFmpegAdapter",
    "OpenCVAdapter", 
    "AudioAdapter",
    "WhisperAdapter",
]