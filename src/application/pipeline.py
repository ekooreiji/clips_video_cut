"""
Video Pipeline - Orquestrador Principal

Responsável por orquestrar todo o processo de detecção e corte de vídeos.
"""

from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
import json

from src.domain.entities.video import VideoDocument
from src.domain.entities.clip import ClipSegment
from src.domain.values.config import ProcessingConfig
from src.domain.use_cases.detect_scene import SceneDetector
from src.domain.use_cases.detect_silence import SilenceDetector
from src.infrastructure.adapters.ffmpeg_adapter import FFmpegAdapter
from src.infrastructure.adapters.whisper_adapter import WhisperAdapter
from src.infrastructure.exporters.json_exporter import JSONExporter
from src.common.exceptions import (
    VideoNotFoundError,
    VideoCorruptedError,
    FFmpegNotFoundError,
)
from src.common.utils.logger import get_logger

logger = get_logger(__name__)


class VideoPipeline:
    """
    Pipeline principal para processamento de vídeos.
    
    Orquestra detectores, processadores e exporters para criar clips
    automaticamente a partir de um vídeo de entrada.
    """
    
    def __init__(self, config: Optional[ProcessingConfig] = None):
        """
        Inicializa o pipeline.
        
        Args:
            config: Configuração de processamento
        """
        self.config = config or ProcessingConfig()
        self.scene_detector = SceneDetector()
        self.silence_detector = SilenceDetector()
        self.ffmpeg = FFmpegAdapter()
        self.whisper = WhisperAdapter()
        self.json_exporter = JSONExporter()
        
        logger.info("Pipeline inicializado")
    
    def process_single(
        self,
        video_path: Path,
        output_dir: Optional[Path] = None
    ) -> Dict[str, Any]:
        """
        Processa um único vídeo.
        
        Args:
            video_path: Caminho do vídeo de entrada
            output_dir: Diretório de saída (opcional)
            
        Returns:
            Dicionário com resultado do processamento
        """
        logger.info(f"Iniciando processamento: {video_path}")
        
        # Validar vídeo
        if not video_path.exists():
            raise VideoNotFoundError(str(video_path))
        
        # Criar documento de vídeo
        video_doc = VideoDocument(path=video_path)
        
        if not video_doc.is_valid_format():
            raise VideoCorruptedError(str(video_path))
        
        # Detectar metadados
        metadata = self.ffmpeg.get_metadata(video_path)
        video_doc.metadata = metadata
        
        # Definir diretório de saída
        if output_dir:
            output_path = output_dir
        else:
            output_path = video_doc.output_directory
        
        # Criar diretório de saída
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Detectar cortes
        clips = self._detect_clips(video_doc)
        
        # Detectar silêncio (se habilitado)
        if self.config.silence.enabled and metadata.has_audio:
            silence_clips = self._detect_silence(video_doc)
            clips.extend(silence_clips)
        
        # Ordenar e mesclar clips sobrepostos
        clips = self._merge_clips(clips)
        
        # Gerar legendas (se habilitado)
        subtitles_path = None
        if self.config.subtitles.enabled and metadata.has_audio:
            subtitles_path = self._generate_subtitles(video_path, output_path)
        
        # Cortar vídeo
        output_files = self._cut_video(video_doc, clips, output_path)
        
        # Gerar relatório
        report = self._generate_report(
            video_doc,
            clips,
            output_files,
            subtitles_path
        )
        
        # Salvar relatório
        report_path = output_path / "report.json"
        self.json_exporter.export(report, report_path)
        
        # Deletar original (se habilitado)
        if not self.config.output.keep_original:
            video_path.unlink()
            logger.info(f"Arquivo original deletado: {video_path}")
        
        result = {
            "video": str(video_path),
            "clips_detected": len(clips),
            "clips": [c.to_dict() for c in clips],
            "report_path": str(report_path),
            "output_files": [str(f) for f in output_files],
            "processing_date": datetime.now().isoformat(),
        }
        
        logger.info(
            f"Processamento concluído: {len(clips)} clips, "
            f"{len(output_files)} arquivos"
        )
        
        return result
    
    def preview(
        self,
        video_path: Path,
        output_dir: Optional[Path] = None
    ) -> Dict[str, Any]:
        """
        Pré-visualiza os pontos de corte sem processar.
        
        Args:
            video_path: Caminho do vídeo
            output_dir: Diretório de saída (opcional)
            
        Returns:
            Dicionário com clips detectados (sem processar)
        """
        logger.info(f"Gerando preview: {video_path}")
        
        video_doc = VideoDocument(path=video_path)
        metadata = self.ffmpeg.get_metadata(video_path)
        video_doc.metadata = metadata
        
        # Detectar cortes
        clips = self._detect_clips(video_doc)
        
        if self.config.silence.enabled and metadata.has_audio:
            silence_clips = self._detect_silence(video_doc)
            clips.extend(silence_clips)
        
        clips = self._merge_clips(clips)
        
        return {
            "video": str(video_path),
            "metadata": {
                "duration": metadata.duration,
                "fps": metadata.fps,
                "resolution": f"{metadata.width}x{metadata.height}",
                "has_audio": metadata.has_audio,
            },
            "clips_detected": len(clips),
            "clips": [c.to_dict() for c in clips],
            "processing_date": datetime.now().isoformat(),
        }
    
    def _detect_clips(self, video_doc: VideoDocument) -> List[ClipSegment]:
        """Detecta clips via análise visual"""
        
        logger.info(f"Config visual_cut.enabled: {self.config.visual_cut.enabled}")
        logger.info(f"Config sensitivity: {self.config.visual_cut.sensitivity}")
        logger.info(f"Config sample_rate: {self.config.visual_cut.sample_rate}")
        logger.info(f"Config min_clip_duration: {self.config.visual_cut.min_clip_duration}")
        
        if not self.config.visual_cut.enabled:
            logger.info("Visual cut desabilitado, retornando []")
            return []
        
        clips = self.scene_detector.detect(
            video_doc.path,
            sensitivity=self.config.visual_cut.sensitivity,
            sample_rate=self.config.visual_cut.sample_rate,
        )
        
        # Filtrar por duração mínima
        min_duration = self.config.visual_cut.min_clip_duration
        if min_duration > 0:
            original_count = len(clips)
            clips = [c for c in clips if c.duration >= min_duration]
            logger.info(f"Filtrados {original_count - len(clips)} clips maiores ou iguais a {min_duration}s")
        
        logger.debug(f"Detectados {len(clips)} clips visuais")
        return clips
    
    def _detect_silence(self, video_doc: VideoDocument) -> List[ClipSegment]:
        """Detecta clips via silêncio em áudio"""
        
        clips = self.silence_detector.detect(
            video_doc.path,
            db_threshold=self.config.silence.db_threshold,
            min_duration=self.config.silence.min_duration,
        )
        
        logger.debug(f"Detectados {len(clips)} clips de silêncio")
        return clips
    
    def _generate_subtitles(
        self,
        video_path: Path,
        output_dir: Path
    ) -> Path:
        """Gera legendas com Whisper"""
        
        video_doc = VideoDocument(path=video_path)
        output_file = output_dir / f"{video_doc.name}.{self.config.subtitles.format}"
        
        self.whisper.generate(
            video_path,
            output_file,
            model=self.config.subtitles.whisper_model,
            format=self.config.subtitles.format,
        )
        
        # Burn subtitles no vídeo (se habilitado)
        if self.config.subtitles.burn:
            self.whisper.burn_subtitles(
                video_path,
                output_file,
                output_dir / f"{video_doc.name}_burned.mp4"
            )
        
        logger.info(f"Legendas geradas: {output_file}")
        return output_file
    
    def _cut_video(
        self,
        video_doc: VideoDocument,
        clips: List[ClipSegment],
        output_dir: Path
    ) -> List[Path]:
        """Corta o vídeo em clips"""
        
        if not clips:
            return []
        
        output_files = []
        
        for clip in clips:
            output_file = output_dir / f"{video_doc.name}_clip_{clip.id:03d}.mp4"
            
            self.ffmpeg.cut(
                video_doc.path,
                clip.start_time,
                clip.end_time,
                output_file,
            )
            
            output_files.append(output_file)
            logger.debug(f"Clip salvo: {output_file}")
        
        return output_files
    
    def _merge_clips(self, clips: List[ClipSegment]) -> List[ClipSegment]:
        """Mescla clips sobrepostos"""
        
        if not clips:
            return []
        
        # Ordenar por start_time
        clips.sort(key=lambda c: c.start_time)
        
        merged = [clips[0]]
        
        for clip in clips[1:]:
            # Verificar sobreposição
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
        
        # Re numerar
        for i, clip in enumerate(merged):
            clip.id = i + 1
        
        return merged
    
    def _generate_report(
        self,
        video_doc: VideoDocument,
        clips: List[ClipSegment],
        output_files: List[Path],
        subtitles_path: Optional[Path]
    ) -> Dict[str, Any]:
        """Gera relatório de processamento"""
        
        return {
            "input_video": str(video_doc.path),
            "input_video_name": video_doc.name,
            "processing_date": datetime.now().isoformat(),
            "options": self.config.to_dict(),
            "metadata": {
                "width": video_doc.metadata.width,
                "height": video_doc.metadata.height,
                "fps": video_doc.metadata.fps,
                "codec": video_doc.metadata.codec,
                "duration": video_doc.metadata.duration,
                "has_audio": video_doc.metadata.has_audio,
            },
            "clips_detected": len(clips),
            "clips": [c.to_dict() for c in clips],
            "output_files": [str(f) for f in output_files],
            "subtitles_file": str(subtitles_path) if subtitles_path else None,
        }