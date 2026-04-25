"""
Scene Detector - Detecção de Mudança de Cena

Use Case para detectar mudanças de cena em vídeos via análise visual.
"""

from pathlib import Path
from typing import List
import numpy as np

from src.domain.entities.clip import ClipSegment, ClipReason
from src.infrastructure.adapters.opencv_adapter import OpenCVAdapter
from src.common.utils.logger import get_logger

logger = get_logger(__name__)


class SceneDetector:
    """
    Caso de uso para detecção de mudanças de cena.
    
    Utiliza análise de diferença entre frames para identificar
   transições de cena.
    """
    
    def __init__(self):
        self.opencv = OpenCVAdapter()
        self.min_clip_length = 10  # frames mínimos
    
    def detect(
        self,
        video_path: Path,
        sensitivity: float = 1.0,
        sample_rate: int = 5
    ) -> List[ClipSegment]:
        """
        Detecta mudanças de cena no vídeo.
        
        Args:
            video_path: Caminho do vídeo
            sensitivity: Fator de sensibilidade (0.3=baixa, 1.0=média, 2.0=alta)
            sample_rate: Analisa a cada N frames
            
        Returns:
            Lista de ClipSegments detectados
        """
        logger.debug(
            f"Detectando cenas: sensitivity={sensitivity}, "
            f"sample_rate={sample_rate}"
        )
        
        # Calcular scores de movimento
        scores, frame_indices = self.opencv.compute_motion_scores(
            video_path,
            sample_rate
        )
        
        if not scores:
            logger.warning("Nenhum frame processado")
            return []
        
        # Suavizar scores
        scores = self._smooth_scores(scores, window=5)
        
        # Calcular thresholds
        mean = np.mean(scores)
        threshold_low = mean * 0.5 * sensitivity
        threshold_high = mean * 1.5 * sensitivity
        
        logger.debug(f"Thresholds: low={threshold_low:.2f}, high={threshold_high:.2f}")
        
        # Detectar clips
        clips = []
        in_clip = False
        
        for i in range(1, len(scores)):
            # Início de clip
            if not in_clip and scores[i] > threshold_high:
                start_frame = frame_indices[i]
                in_clip = True
            
            # Fim de clip
            elif in_clip and scores[i] < threshold_low:
                end_frame = frame_indices[i]
                
                clip_frames = end_frame - start_frame
                
                if clip_frames > self.min_clip_length:
                    # Converter para timestamp
                    fps = self.opencv.get_fps(video_path)
                    start_time = start_frame / fps
                    end_time = end_frame / fps
                    
                    clips.append(ClipSegment(
                        id=len(clips) + 1,
                        start_time=start_time,
                        end_time=end_time,
                        reason=ClipReason.SCENE_CHANGE,
                        scene_score=scores[i]
                    ))
                
                in_clip = False
        
        logger.info(f"Detectados {len(clips)} clips de cena")
        
        return clips
    
    def _smooth_scores(self, scores: np.ndarray, window: int = 5) -> np.ndarray:
        """
        Suaviza scores com média móvel.
        
        Args:
            scores: Array de scores
            window: Tamanho da janela
            
        Returns:
            Scores suavizados
        """
        return np.convolve(scores, np.ones(window) / window, mode='same')