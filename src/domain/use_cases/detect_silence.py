"""
Silence Detector - Detecção de Silêncio em Áudio

Use Case para detectar silêncio em áudio de vídeos.
"""

from pathlib import Path
from typing import List, Tuple

from src.domain.entities.clip import ClipSegment, ClipReason
from src.infrastructure.adapters.audio_adapter import AudioAdapter
from src.common.utils.logger import get_logger

logger = get_logger(__name__)


class SilenceDetector:
    """
    Caso de uso para detecção de silêncio em áudio.
    
    Utiliza análise de amplitude para identificar
    trechos silenciosos.
    """
    
    def __init__(self):
        self.audio_adapter = AudioAdapter()
    
    def detect(
        self,
        video_path: Path,
        db_threshold: int = -40,
        min_duration: float = 0.5
    ) -> List[ClipSegment]:
        """
        Detecta silêncio no áudio do vídeo.
        
        Args:
            video_path: Caminho do vídeo
            db_threshold: Threshold em dB para silêncio
            min_duration: Duração mínima do silêncio em segundos
            
        Returns:
            Lista de ClipSegments de silêncio
        """
        logger.debug(
            f"Detectando silêncio: threshold={db_threshold}dB, "
            f"min_duration={min_duration}s"
        )
        
        # Detectar ranges de silêncio
        silence_ranges = self.audio_adapter.detect_silence(
            video_path,
            db_threshold=db_threshold,
            min_duration=min_duration
        )
        
        if not silence_ranges:
            logger.info("Nenhum silêncio detectado")
            return []
        
        # Converter para ClipSegments
        clips = []
        
        for i, (start_time, end_time) in enumerate(silence_ranges):
            duration = end_time - start_time
            
            # Só incluir se duração mínima
            if duration >= min_duration:
                clips.append(ClipSegment(
                    id=i + 1,
                    start_time=start_time,
                    end_time=end_time,
                    reason=ClipReason.SILENCE_REMOVAL,
                ))
        
        logger.info(f"Detectados {len(clips)} clips de silêncio")
        
        return clips
    
    def get_ranges(
        self,
        video_path: Path,
        db_threshold: int = -40,
        min_duration: float = 0.5
    ) -> List[Tuple[float, float]]:
        """
        Retorna ranges de silêncio apenas (sem criar clips).
        
        Args:
            video_path: Caminho do vídeo
            db_threshold: Threshold em dB
            min_duration: Duração mínima
            
        Returns:
            Lista de (start_time, end_time)
        """
        return self.audio_adapter.detect_silence(
            video_path,
            db_threshold=db_threshold,
            min_duration=min_duration
        )