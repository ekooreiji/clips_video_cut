"""
Batch Processor - Processamento em Lote

Responsável por processar múltiplos vídeos simultaneamente.
"""

from pathlib import Path
from typing import List, Dict, Any
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

from src.domain.values.config import ProcessingConfig
from src.application.pipeline import VideoPipeline
from src.common.utils.logger import get_logger

logger = get_logger(__name__)


def _process_worker(args: tuple) -> Dict[str, Any]:
    """
    Worker function para multiprocessing.
    
    Args:
        args: (video_path, config_json, output_dir)
        
    Returns:
        Resultado do processamento
    """
    video_path, config_dict, output_dir = args
    
    pipeline = VideoPipeline(config=ProcessingConfig(**config_dict))
    
    try:
        result = pipeline.process_single(video_path, output_dir)
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e), "video": str(video_path)}


class BatchProcessor:
    """
    Processador em lote para múltiplos vídeos.
    
    Utiliza multiprocessing para processar até max_workers
    vídeos simultaneamente.
    """
    
    def __init__(self, config: ProcessingConfig = None):
        """
        Inicializa o processador em lote.
        
        Args:
            config: Configuração de processamento
        """
        self.config = config or ProcessingConfig()
        self.max_workers = self.config.output.max_workers
    
    def process_directory(
        self,
        directory: Path,
        extensions: List[str] = None,
        recursive: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Processa todos os vídeos de um diretório.
        
        Args:
            directory: Diretório com vídeos
            extensions: Extensões a processar
            recursive: Processar subdiretórios
            
        Returns:
            Lista de resultados
        """
        if extensions is None:
            extensions = ['.mp4', '.mkv', '.avi', '.webm', '.mov']
        
        # Coletar vídeos
        videos = []
        for ext in extensions:
            if recursive:
                videos.extend(directory.rglob(f"*{ext}"))
            else:
                videos.extend(directory.glob(f"*{ext}"))
        
        logger.info(f"Encontrados {len(videos)} vídeos para processar")
        
        # Processar com paralelização
        results = self.process_batch(videos)
        
        return results
    
    def process_batch(
        self,
        videos: List[Path]
    ) -> List[Dict[str, Any]]:
        """
        Processa uma lista de vídeos em paralelo.
        
        Args:
            videos: Lista de caminhos de vídeo
            
        Returns:
            Lista de resultados
        """
        if not videos:
            return []
        
        # Limitarworkers
        n_workers = min(self.max_workers, len(videos), 10)
        
        logger.info(f"Iniciando processamento em paralelo ({n_workers} workers)")
        
        # Preparar argumentos
        args_list = [
            (video, self.config.to_dict(), None)
            for video in videos
        ]
        
        results = []
        
        with ProcessPoolExecutor(max_workers=n_workers) as executor:
            futures = {
                executor.submit(_process_worker, args): args[0]
                for args in args_list
            }
            
            for future in as_completed(futures):
                video = futures[future]
                
                try:
                    result = future.result()
                    
                    if result["success"]:
                        logger.info(f"✓ {video.name}")
                        results.append(result["result"])
                    else:
                        logger.error(f"✗ {video.name}: {result['error']}")
                        results.append(result)
                
                except Exception as e:
                    logger.exception(f"Erro em {video.name}")
                    results.append({
                        "success": False,
                        "error": str(e),
                        "video": str(video)
                    })
        
        # Contar sucessos
        successes = sum(1 for r in results if r.get("success", True))
        logger.info(
            f"Processamento concluído: {successes}/{len(videos)} успешно"
        )
        
        return results
    
    def merge_reports(
        self,
        results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Mescla relatórios de múltiplos processamentos.
        
        Args:
            results: Lista de resultados
            
        Returns:
            Relatório mesclado
        """
        total_clips = 0
        total_files = 0
        successful = 0
        failed = 0
        
        merged_clips = []
        
        for result in results:
            if result.get("success", True):
                successful += 1
                total_clips += result.get("clips_detected", 0)
                total_files += len(result.get("output_files", []))
            else:
                failed += 1
        
        return {
            "total_videos": len(results),
            "successful": successful,
            "failed": failed,
            "total_clips": total_clips,
            "total_files": total_files,
        }