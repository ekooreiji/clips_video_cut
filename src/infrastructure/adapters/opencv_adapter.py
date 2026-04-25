"""
OpenCV Adapter - Processamento de Frames com OpenCV

Adapter para análise de frames usando OpenCV.
"""

from pathlib import Path
from typing import List, Tuple
import numpy as np

import cv2
import imageio_ffmpeg

from src.common.exceptions import VideoCorruptedError, VideoNotFoundError
from src.common.utils.logger import get_logger

logger = get_logger(__name__)


def get_ffmpeg_path() -> str:
    """Retorna o caminho do FFmpeg"""
    return imageio_ffmpeg.get_ffmpeg_exe()


class OpenCVAdapter:
    """
    Adapter para processamento de frames com OpenCV.
    
    Responsibilities:
    - Calcular scores de movimento entre frames
    - Detectar mudanças de cena
    - Obter FPS do vídeo
    """
    
    def __init__(self):
        pass
    
    def compute_motion_scores(
        self,
        video_path: Path,
        sample_rate: int = 5
    ) -> Tuple[List[float], List[int]]:
        """
        Calcula scores de movimento entre frames.
        
        Args:
            video_path: Caminho do vídeo
            sample_rate: Avaliar a cada N frames
            
        Returns:
            Tupla de (scores, frame_indices)
        """
        if not video_path.exists():
            raise VideoNotFoundError(str(video_path))
        
        cap = cv2.VideoCapture(str(video_path))
        
        if not cap.isOpened():
            raise VideoCorruptedError(str(video_path))
        
        scores = []
        frame_indices = []
        frame_id = 0
        
        # Ler primeiro frame
        ret, prev_frame = cap.read()
        if not ret:
            cap.release()
            return [], []
        
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Sample
            if frame_id % sample_rate == 0 and frame_id > 0:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Calcular diferença
                diff = cv2.absdiff(prev_gray, gray)
                score = np.mean(diff)
                
                scores.append(score)
                frame_indices.append(frame_id)
                
                prev_gray = gray
            
            frame_id += 1
        
        cap.release()
        
        return scores, frame_indices
    
    def detect_scene_changes(
        self,
        video_path: Path,
        sample_rate: int = 5,
        threshold_multiplier: float = 1.5
    ) -> List[Tuple[int, int]]:
        """
        Detecta mudanças de cena.
        
        Args:
            video_path: Caminho do vídeo
            sample_rate: Avaliar a cada N frames
            threshold_multiplier: Multiplicador do threshold
            
        Returns:
            Lista de (start_frame, end_frame)
        """
        scores, frame_indices = self.compute_motion_scores(
            video_path,
            sample_rate
        )
        
        if not scores:
            return []
        
        # Suavizar
        scores = self._smooth(scores, window=5)
        
        # Thresholds
        mean = np.mean(scores)
        low = mean * 0.5
        high = mean * threshold_multiplier
        
        # Detectar
        scenes = []
        in_scene = False
        
        for i in range(1, len(scores)):
            if not in_scene and scores[i] > high:
                start = frame_indices[i]
                in_scene = True
            elif in_scene and scores[i] < low:
                end = frame_indices[i]
                
                if end - start > 10:
                    scenes.append((start, end))
                
                in_scene = False
        
        return scenes
    
    def _smooth(self, scores: List[float], window: int = 5) -> np.ndarray:
        """Suaviza scores com média móvel"""
        return np.convolve(
            np.array(scores),
            np.ones(window) / window,
            mode='same'
        )
    
    def get_fps(self, video_path: Path) -> float:
        """Obtém FPS do vídeo"""
        cap = cv2.VideoCapture(str(video_path))
        
        if not cap.isOpened():
            return 30.0  # Fallback: FPS padrão
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()
        
        # Fallback para FPS inválido
        if fps <= 0 or fps is None:
            logger.warning(f"FPS inválido para {video_path}, usando 30.0 como fallback")
            return 30.0
        
        return fps
    
    def get_frame_at(
        self,
        video_path: Path,
        timestamp: float
    ) -> np.ndarray:
        """
        Extrai frame em um timestamp específico.
        
        Args:
            video_path: Caminho do vídeo
            timestamp: Tempo em segundos
            
        Returns:
            Array numpy do frame
        """
        cap = cv2.VideoCapture(str(video_path))
        
        if not cap.isOpened():
            cap.release()
            raise VideoCorruptedError(str(video_path))
        
        # Converter para frame
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_number = int(timestamp * fps)
        
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            raise VideoCorruptedError(f"Frame não encontrado em {timestamp}s")
        
        return frame
    
    def get_thumbnail(
        self,
        video_path: Path,
        timestamp: float,
        width: int = 160
    ) -> np.ndarray:
        """
        Gera thumbnail em um timestamp.
        
        Args:
            video_path: Caminho do vídeo
            timestamp: Tempo em segundos
            width: Largura do thumbnail
            
        Returns:
            Thumbnail redimensionado
        """
        frame = self.get_frame_at(video_path, timestamp)
        
        # Redimensionar
        h, w = frame.shape[:2]
        ratio = width / w
        height = int(h * ratio)
        
        thumbnail = cv2.resize(frame, (width, height))
        
        return thumbnail
    
    def extract_audio_wav(
        self,
        video_path: Path,
        output_wav: Path
    ):
        """
        Extrai áudio como WAV usando subprocess.
        
        Args:
            video_path: Vídeo de entrada
            output_wav: Arquivo WAV de saída
        """
        import subprocess
        
        # Usar ffmpeg para extrair
        cmd = [
            get_ffmpeg_path(),
            "-y",
            "-i", str(video_path),
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            str(output_wav)
        ]
        
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)