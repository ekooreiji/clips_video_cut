"""
SRT Exporter - Exportador de Legendas SRT
"""

from pathlib import Path
from typing import List, Dict, Any

from src.domain.entities.clip import ClipSegment
from src.domain.values.timestamp import Timestamp


class SRTExporter:
    """Exportador de legendas em formato SRT"""
    
    def export(
        self,
        segments: List[Dict[str, Any]],
        output_path: Path
    ):
        """
        Exporta segmentos para formato SRT.
        
        Args:
            segments: Lista de dicionários com {start, end, text}
            output_path: Arquivo de saída
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(segments, 1):
                # Timestamp
                start_ts = Timestamp(seconds=segment['start'])
                end_ts = Timestamp(seconds=segment['end'])
                
                # Escrever
                f.write(f"{i}\n")
                f.write(f"{start_ts.srt_format} --> {end_ts.srt_format}\n")
                f.write(f"{segment['text']}\n\n")
    
    def export_from_clips(
        self,
        clips: List[ClipSegment],
        texts: Dict[int, str],
        output_path: Path
    ):
        """
        Exporta clips com textos em formato SRT.
        
        Args:
            clips: Lista de ClipSegments
            texts: Dicionário de {clip_id: texto}
            output_path: Arquivo de saída
        """
        segments = []
        
        for clip in clips:
            text = texts.get(clip.id, "")
            segments.append({
                'start': clip.start_time,
                'end': clip.end_time,
                'text': text
            })
        
        self.export(segments, output_path)