"""
FFmpeg Adapter - Processamento de Vídeo com FFmpeg

Adapter para processar vídeos usando FFmpeg via imageio-ffmpeg.
"""

from pathlib import Path
from typing import Optional, List, Dict, Any
import subprocess
import json
import os

import imageio_ffmpeg

from src.domain.entities.video import VideoDocument, VideoMetadata
from src.common.exceptions import FFmpegNotFoundError
from src.common.utils.logger import get_logger

logger = get_logger(__name__)


def get_ffmpeg_path() -> str:
    """Retorna o caminho do FFmpeg"""
    return imageio_ffmpeg.get_ffmpeg_exe()


class FFmpegAdapter:
    """
    Adapter para processamento de vídeos com FFmpeg.
    
    Responsibilities:
    - Obter metadados do vídeo
    - Cortar vídeos
    - Remover silêncio
    - Normalizar áudio
    """
    
    def __init__(self):
        """Inicializa com caminho do FFmpeg"""
        self.ffmpeg_path = get_ffmpeg_path()
        logger.debug(f"FFmpeg: {self.ffmpeg_path}")
    
    def _run_ffmpeg(self, args: List[str], check: bool = True) -> subprocess.CompletedProcess:
        """Executa comando FFmpeg"""
        cmd = [self.ffmpeg_path] + args
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        
        if check and result.returncode != 0:
            error = result.stderr.decode(errors='ignore')
            logger.error(f"FFmpeg error: {error}")
            raise Exception(f"FFmpeg error: {error}")
        
        return result
    
    def get_metadata(self, video_path: Path) -> VideoMetadata:
        """
        Obtém metadados do vídeo usando ffprobe.
        
        Args:
            video_path: Caminho do vídeo
            
        Returns:
            VideoMetadata com informações do vídeo
        """
        cmd = [
            self.ffmpeg_path,
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            str(video_path)
        ]
        # Substituir ffprobe por ffmpeg -i
        cmd[0] = self.ffmpeg_path
        
        # Usar ffmpeg para obter info
        cmd = [
            self.ffmpeg_path,
            "-i", str(video_path),
            "-hide_banner"
        ]
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        
        # Parse Output from stderr
        stderr = result.stderr.decode(errors='ignore')
        
        # Tentar obter info de outra forma - usar opencv
        import cv2
        cap = cv2.VideoCapture(str(video_path))
        
        if not cap.isOpened():
            return VideoMetadata(width=0, height=0, fps=0, codec="unknown")
        
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps if fps > 0 else 0
        
        # Verificar se tem áudio
        has_audio = cap.get(cv2.CAP_PROP_AUDIO_STREAM) >= 0
        
        cap.release()
        
        return VideoMetadata(
            width=width,
            height=height,
            fps=fps,
            codec="unknown",
            duration=duration,
            has_audio=has_audio,
        )
    
    def _parse_fps(self, fps_str: str) -> float:
        """Converte string de FPS para float"""
        try:
            num, denom = fps_str.split("/")
            return float(num) / float(denom)
        except:
            return 0.0
    
    def cut(
        self,
        input_path: Path,
        start_time: float,
        end_time: float,
        output_path: Path,
        codec: str = "copy"
    ):
        """
        Corta vídeo em um intervalo de tempo.
        
        Args:
            input_path: Vídeo de entrada
            start_time: Tempo inicial em segundos
            end_time: Tempo final em segundos
            output_path: Vídeo de saída
            codec: Codec para output (copy para sem recodificação)
        """
        cmd = [
            self.ffmpeg_path,
            "-y",  # Sobrescrever
            "-i", str(input_path),
            "-ss", str(start_time),
            "-to", str(end_time),
            "-c", codec,
            "-avoid_negative_ts", "make_zero",
            str(output_path)
        ]
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        
        if result.returncode != 0:
            error = result.stderr.decode()
            logger.error(f"Erro ao cortar: {error}")
            raise Exception(f"Erro ao cortar vídeo: {error}")
        
        logger.debug(f"Vídeo cortado: {output_path}")
    
    def cut_multiple(
        self,
        input_path: Path,
        clips: List[tuple],
        output_dir: Path,
        name_prefix: str = "clip"
    ) -> List[Path]:
        """
        Corta vídeo em múltiplos clips.
        
        Args:
            input_path: Vídeo de entrada
            clips: Lista de (start_time, end_time)
            output_dir: Diretório de saída
            name_prefix: Prefixo para nome dos arquivos
            
        Returns:
            Lista de caminhos de saída
        """
        output_files = []
        
        for i, (start_time, end_time) in enumerate(clips):
            output_file = output_dir / f"{name_prefix}_{i+1:03d}.mp4"
            
            self.cut(input_path, start_time, end_time, output_file)
            
            output_files.append(output_file)
        
        return output_files
    
    def remove_silence(
        self,
        input_path: Path,
        output_path: Path,
        silence_threshold: float = -40,
        min_duration: float = 0.5
    ):
        """
        Remove silêncio do áudio.
        
        Args:
            input_path: Vídeo de entrada
            output_path: Vídeo de saída
            silence_threshold: Threshold em dB
            min_duration: Duração mínima do silêncio
        """
        # Usar silenceremove filter do FFmpeg
        cmd = [
            self.ffmpeg_path,
            "-y",
            "-i", str(input_path),
            "-af", f"silenceremove=start_periods=-1:start_duration={min_duration}:start_threshold={silence_threshold}dB",
            "-c:v", "copy",
            str(output_path)
        ]
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        
        if result.returncode != 0:
            error = result.stderr.decode()
            logger.error(f"Erro ao remover silêncio: {error}")
            raise Exception(f"Erro ao remover silêncio: {error}")
        
        logger.debug(f"Silêncio removido: {output_path}")
    
    def normalize_audio(
        self,
        input_path: Path,
        output_path: Path,
        target_level: float = -20.0
    ):
        """
        Normaliza volume do áudio.
        
        Args:
            input_path: Vídeo de entrada
            output_path: Vídeo de saída
            target_level: Nível alvo em dB
        """
        cmd = [
            self.ffmpeg_path,
            "-y",
            "-i", str(input_path),
            "-af", f"loudnorm=I={target_level}",
            "-c:v", "copy",
            str(output_path)
        ]
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        
        if result.returncode != 0:
            error = result.stderr.decode()
            logger.error(f"Erro ao normalizar: {error}")
            raise Exception(f"Erro ao normalizar áudio: {error}")
        
        logger.debug(f"Áudio normalizado: {output_path}")
    
    def extract_audio(
        self,
        video_path: Path,
        output_path: Path
    ):
        """
        Extrai áudio do vídeo como arquivo WAV.
        
        Args:
            video_path: Vídeo de entrada
            output_path: Arquivo de saída WAV
        """
        cmd = [
            self.ffmpeg_path,
            "-y",
            "-i", str(video_path),
            "-vn",  # Sem vídeo
            "-acodec", "pcm_s16le",
            str(output_path)
        ]
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        
        if result.returncode != 0:
            error = result.stderr.decode()
            raise Exception(f"Erro ao extrair áudio: {error}")
        
        logger.debug(f"Áudio extraído: {output_path}")