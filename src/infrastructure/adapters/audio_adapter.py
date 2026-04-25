"""
Audio Adapter - Processamento de Áudio

Adapter para análise e processamento de áudio usando scipy e subprocess.
"""

from pathlib import Path
from typing import List, Tuple, Optional
import tempfile
import subprocess

import numpy as np
from scipy.io import wavfile
from scipy import signal

from src.infrastructure.adapters.opencv_adapter import OpenCVAdapter
from src.common.utils.logger import get_logger

logger = get_logger(__name__)


class AudioAdapter:
    """
    Adapter para processamento de áudio.
    
    Responsibilities:
    - Detectar silêncio
    - Normalizar áudio
    - Obter informações de áudio
    """
    
    def __init__(self):
        self.opencv = OpenCVAdapter()
    
    def detect_silence(
        self,
        video_path: Path,
        db_threshold: int = -40,
        min_duration: float = 0.5
    ) -> List[Tuple[float, float]]:
        """
        Detecta trechos de silêncio no áudio.
        
        Args:
            video_path: Caminho do vídeo
            db_threshold: Threshold em dB para silêncio
            min_duration: Duração mínima em segundos
            
        Returns:
            Lista de (start_time, end_time) em segundos
        """
        tmp_wav: Optional[Path] = None
        
        try:
            # Extrair áudio como WAV temporário
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
                tmp_wav = Path(tmp.name)
            
            self._extract_audio(video_path, tmp_wav)
            
            # Carregar áudio
            sample_rate, audio_data = wavfile.read(tmp_wav)
            
            # Converter para mono se estéreo
            if len(audio_data.shape) > 1:
                audio_data = audio_data.mean(axis=1)
            
            # Normalizar para float
            audio_float = audio_data.astype(np.float32) / 32768.0
            
            # Calcular RMS em janelas
            window_size = int(sample_rate * 0.05)  # 50ms
            hop_size = window_size // 2
            
            rms = []
            for i in range(0, len(audio_float) - window_size, hop_size):
                window = audio_float[i:i + window_size]
                rms.append(np.sqrt(np.mean(window ** 2)))
            
            rms = np.array(rms)
            
            # Converter para dB
            # Evitar log de zero
            rms = np.maximum(rms, 1e-10)
            db = 20 * np.log10(rms)
            
            # Detectar silêncio
            silence_threshold = db_threshold
            is_silent = db < silence_threshold
            
            # Encontrar regiões silenciosas
            silence_ranges = []
            in_silence = False
            start_sample = 0
            
            for i, silent in enumerate(is_silent):
                if silent and not in_silence:
                    in_silence = True
                    start_sample = i
                elif not silent and in_silence:
                    in_silence = False
                    end_sample = i
                    
                    # Converter para tempo
                    start_time = (start_sample * hop_size) / sample_rate
                    end_time = (end_sample * hop_size) / sample_rate
                    
                    # Verificar duração mínima
                    if end_time - start_time >= min_duration:
                        silence_ranges.append((start_time, end_time))
            
            logger.debug(f"Detectados {len(silence_ranges)} trechos de silêncio")
            
            return silence_ranges
        
        finally:
            # Limpar arquivo temporário de forma robusta
            if tmp_wav is not None:
                self._cleanup_temp_file(tmp_wav)
    
    def _cleanup_temp_file(self, path: Path) -> None:
        """Limpa arquivo temporário de forma segura"""
        try:
            if path and path.exists():
                path.unlink()
                logger.debug(f"Arquivo temporário limpo: {path}")
        except Exception as e:
            logger.warning(f"Não foi possível limpar {path}: {e}")
    
    def _extract_audio(self, video_path: Path, output_wav: Path):
        """Extrai áudio do vídeo usando ffmpeg"""
        import imageio_ffmpeg
        
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        
        cmd = [
            ffmpeg_path,
            "-y",
            "-i", str(video_path),
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            str(output_wav)
        ]
        
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    def get_audio_info(
        self,
        video_path: Path
    ) -> dict:
        """
        Obtém informações do áudio.
        
        Args:
            video_path: Caminho do vídeo
            
        Returns:
            Dicionário com informações
        """
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            tmp_wav = Path(tmp.name)
        
        try:
            self._extract_audio(video_path, tmp_wav)
            
            sample_rate, audio_data = wavfile.read(tmp_wav)
            
            return {
                "duration": len(audio_data) / sample_rate,
                "sample_rate": sample_rate,
                "channels": 2 if len(audio_data.shape) > 1 else 1,
                "dtype": str(audio_data.dtype),
            }
        
        finally:
            if tmp_wav.exists():
                try:
                    tmp_wav.unlink()
                except:
                    pass
    
    def extract_audio(
        self,
        video_path: Path,
        output_path: Path,
        format: str = "wav"
    ):
        """
        Extrai áudio do vídeo.
        
        Args:
            video_path: Vídeo de entrada
            output_path: Arquivo de saída
            format: Formato de saída (wav, mp3)
        """
        self._extract_audio(video_path, output_path)
    
    def normalize(
        self,
        audio_data: np.ndarray,
        target_dbfs: float = -20.0
    ) -> np.ndarray:
        """
        Normaliza áudio para nível específico.
        
        Args:
            audio_data: Dados do áudio
            target_dbfs: Nível alvo em dBFS
            
        Returns:
            Áudio normalizado
        """
        # Calcular RMS atual
        rms = np.sqrt(np.mean(audio_data ** 2))
        
        # Calcular gain
        if rms > 0:
            target_rms = 10 ** (target_dbfs / 20)
            gain = target_rms / rms
            return audio_data * gain
        
        return audio_data