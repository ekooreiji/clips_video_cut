"""
Whisper Adapter - Legendas Automáticas

Adapter para geração de legendas usando Whisper local.
"""

from pathlib import Path
from typing import Optional
import subprocess

import whisper

import imageio_ffmpeg

from src.common.exceptions import WhisperError
from src.common.utils.logger import get_logger

logger = get_logger(__name__)


def get_ffmpeg_path() -> str:
    """Retorna o caminho do FFmpeg"""
    return imageio_ffmpeg.get_ffmpeg_exe()


class WhisperAdapter:
    """
    Adapter para geração de legendas com Whisper.
    
    Responsibilities:
    - Transcrever áudio para texto
    - Gerar legendas em formato SRT/VTT
    - Inserir legendas no vídeo
    """
    
    def __init__(self):
        self.models = {}
    
    def _get_model(self, model_name: str = "base"):
        """
        Obtém ou carrega modelo Whisper.
        
        Args:
            model_name: Nome do modelo (tiny, base, small, medium, large)
            
        Returns:
            Modelo Whisper carregado
        """
        if model_name not in self.models:
            logger.info(f"Carregando modelo Whisper: {model_name}")
            self.models[model_name] = whisper.load_model(model_name)
        
        return self.models[model_name]
    
    def generate(
        self,
        video_path: Path,
        output_path: Path,
        model: str = "base",
        format: str = "srt"
    ):
        """
        Gera legendas a partir do vídeo.
        
        Args:
            video_path: Vídeo de entrada
            output_path: Arquivo de saída (SRT/VTT)
            model: Modelo Whisper a usar
            format: Formato de saída (srt, vtt)
        """
        try:
            # Carregar modelo
            model = self._get_model(model)
            
            logger.info(f"Transcrevendo: {video_path}")
            
            # Transcrever
            result = model.transcribe(str(video_path))
            
            # Gerar formato
            if format.lower() == "srt":
                self._save_srt(result, output_path)
            elif format.lower() == "vtt":
                self._save_vtt(result, output_path)
            else:
                raise ValueError(f"Formato não suportado: {format}")
            
            logger.info(f"Legendas geradas: {output_path}")
        
        except Exception as e:
            logger.error(f"Erro ao gerar legendas: {e}")
            raise WhisperError(str(e), str(video_path))
    
    def _save_srt(self, result: dict, output_path: Path):
        """Salva resultado em formato SRT"""
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(result['segments'], 1):
                # Timestamp
                start = self._format_srt_timestamp(segment['start'])
                end = self._format_srt_timestamp(segment['end'])
                
                # Texto
                text = segment['text'].strip()
                
                # Escrever
                f.write(f"{i}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{text}\n\n")
    
    def _save_vtt(self, result: dict, output_path: Path):
        """Salva resultado em formato VTT"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("WEBVTT\n\n")
            
            for segment in result['segments']:
                start = self._format_vtt_timestamp(segment['start'])
                end = self._format_vtt_timestamp(segment['end'])
                text = segment['text'].strip()
                
                f.write(f"{start} --> {end}\n")
                f.write(f"{text}\n\n")
    
    def _format_srt_timestamp(self, seconds: float) -> str:
        """Formata timestamp para SRT"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        millis = int((secs - int(secs)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{int(secs):02d},{millis:03d}"
    
    def _format_vtt_timestamp(self, seconds: float) -> str:
        """Formata timestamp para VTT"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        millis = int((secs - int(secs)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{int(secs):02d}.{millis:03d}"
    
    def burn_subtitles(
        self,
        video_path: Path,
        subtitle_path: Path,
        output_path: Path
    ):
        """
        Insere legendas no vídeo (burn subtitles).
        
        Args:
            video_path: Vídeo de entrada
            subtitle_path: Arquivo de legendas
            output_path: Vídeo de saída
        """
        # Usar ffmpeg para queimar legendas
        cmd = [
            get_ffmpeg_path(),
            "-y",
            "-i", str(video_path),
            "-vf", f"subtitles='{subtitle_path}'",
            "-c:a", "copy",
            str(output_path)
        ]
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        
        if result.returncode != 0:
            error = result.stderr.decode()
            logger.error(f"Erro ao inserir legendas no vídeo: {error}")
            raise WhisperError(f"Erro ao inserir legendas: {error}")
        
        logger.info(f"Legendas inseridas: {output_path}")