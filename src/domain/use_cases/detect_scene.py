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
    transições de cena (scene cuts) e movimento.
    """
    
    def __init__(self):
        self.opencv = OpenCVAdapter()
    
    def detect(
        self,
        video_path: Path,
        sensitivity: float = 1.0,
        sample_rate: int = 5,
        scene_cut_threshold: float = 0.5,
        min_scene_frames: int = 10,
        detect_motion: bool = True
    ) -> List[ClipSegment]:
        """
        Detecta mudanças de cena no vídeo.
        
        Args:
            video_path: Caminho do vídeo
            sensitivity: Fator de sensibilidade (0.3=baixa, 1.0=média, 2.0=alta)
            sample_rate: Analisa a cada N frames
            scene_cut_threshold: Limiar para scene cut (0.0-1.0)
            min_scene_frames: Frames mínimos por cena
            detect_motion: Ativar detecção de movimento
            
        Returns:
            Lista de ClipSegments detectados
        """
        logger.debug(
            f"Detectando cenas: sensitivity={sensitivity}, "
            f"sample_rate={sample_rate}, "
            f"scene_cut_threshold={scene_cut_threshold}, "
            f"min_scene_frames={min_scene_frames}, "
            f"detect_motion={detect_motion}"
        )
        
        # Detectar scene cuts (cortes limpos)
        scene_cut_clips = self._detect_scene_cuts(
            video_path,
            scene_cut_threshold,
            min_scene_frames,
            sample_rate
        )
        
        logger.info(f"Detectados {len(scene_cut_clips)} scene cuts")
        
        # Detectar motion (se habilitado)
        motion_clips = []
        if detect_motion:
            motion_clips = self._detect_motion(
                video_path,
                sensitivity,
                sample_rate
            )
            logger.info(f"Detectados {len(motion_clips)} clips de movimento")
        
        # Mesclar clips
        all_clips = scene_cut_clips + motion_clips
        
        if not all_clips:
            logger.warning("Nenhuma mudança de cena detectada")
            return []
        
        # Ordenar por tempo
        all_clips.sort(key=lambda c: c.start_time)
        
        # Mesclar clips sobrepostos
        clips = self._merge_clips(all_clips)
        
        logger.info(f"Total de {len(clips)} clips após mesclagem")
        
        return clips
    
    def _detect_scene_cuts(
        self,
        video_path: Path,
        threshold: float,
        min_frames: int,
        sample_rate: int
    ) -> List[ClipSegment]:
        """
        Detecta scene cuts (cortes limpos).
        
        Args:
            video_path: Caminho do vídeo
            threshold: Limiar (0.0-1.0)
            min_frames: Frames mínimos por cena
            sample_rate: Taxa de amostragem
            
        Returns:
            Lista de ClipSegments
        """
        logger.debug(f"Detectando scene cuts: threshold={threshold}")
        
        # Calcular diferença entre frames consecutivos
        diffs, frame_indices = self.opencv.compute_frame_diffs(
            video_path,
            sample_rate
        )
        
        if not diffs:
            return []
        
        # Calcular threshold absoluto baseado na média
        mean_diff = np.mean(diffs)
        absolute_threshold = mean_diff * (1.0 + threshold)
        
        logger.debug(f"Scene cut threshold: absolute={absolute_threshold:.2f}, mean={mean_diff:.2f}")
        
        # Detectar cortes
        clips = []
        scene_start = None
        
        for i in range(1, len(diffs)):
            # Scene cut detectado
            if diffs[i] > absolute_threshold:
                if scene_start is None:
                    scene_start = frame_indices[i]
            else:
                # Fim da cena
                if scene_start is not None:
                    end_frame = frame_indices[i]
                    clip_frames = end_frame - scene_start
                    
                    if clip_frames >= min_frames:
                        fps = self.opencv.get_fps(video_path)
                        clips.append(ClipSegment(
                            id=len(clips) + 1,
                            start_time=scene_start / fps,
                            end_time=end_frame / fps,
                            reason=ClipReason.SCENE_CHANGE,
                            scene_score=diffs[i]
                        ))
                    scene_start = None
        
        return clips
    
    def _detect_motion(
        self,
        video_path: Path,
        sensitivity: float,
        sample_rate: int
    ) -> List[ClipSegment]:
        """
        Detecta movimento entre frames.
        
        Args:
            video_path: Caminho do vídeo
            sensitivity: Sensibilidade
            sample_rate: Taxa de amostragem
            
        Returns:
            Lista de ClipSegments
        """
        # Calcular scores de movimento
        scores, frame_indices = self.opencv.compute_motion_scores(
            video_path,
            sample_rate
        )
        
        if not scores:
            return []
        
        # Suavizar scores
        scores = self._smooth_scores(scores, window=5)
        
        # Calcular thresholds
        mean = np.mean(scores)
        threshold_low = mean * 0.5 * sensitivity
        threshold_high = mean * 1.5 * sensitivity
        
        logger.debug(f"Motion thresholds: low={threshold_low:.2f}, high={threshold_high:.2f}")
        
        # Detectar clips
        clips = []
        in_clip = False
        
        for i in range(1, len(scores)):
            if not in_clip and scores[i] > threshold_high:
                start_frame = frame_indices[i]
                in_clip = True
            
            elif in_clip and scores[i] < threshold_low:
                end_frame = frame_indices[i]
                clip_frames = end_frame - start_frame
                
                if clip_frames > 10:  # min_clip_length
                    fps = self.opencv.get_fps(video_path)
                    clips.append(ClipSegment(
                        id=len(clips) + 1,
                        start_time=start_frame / fps,
                        end_time=end_frame / fps,
                        reason=ClipReason.SCENE_CHANGE,
                        scene_score=scores[i]
                    ))
                
                in_clip = False
        
        return clips
    
    def _merge_clips(self, clips: List[ClipSegment]) -> List[ClipSegment]:
        """Mescla clips sobrepostos"""
        
        if not clips:
            return []
        
        # Ordenar por start_time
        clips.sort(key=lambda c: c.start_time)
        
        merged = [clips[0]]
        
        for clip in clips[1:]:
            if clip.start_time < merged[-1].end_time:
                # Mesclar
                merged[-1] = ClipSegment(
                    id=merged[-1].id,
                    start_time=merged[-1].start_time,
                    end_time=max(merged[-1].end_time, clip.end_time),
                    reason=merged[-1].reason,
                )
            else:
                merged.append(clip)
        
        # Renumerar
        for i, clip in enumerate(merged):
            clip.id = i + 1
        
        return merged
    
    def _smooth_scores(self, scores: np.ndarray, window: int = 5) -> np.ndarray:
        """Suaviza scores com média móvel"""
        return np.convolve(scores, np.ones(window) / window, mode='same')