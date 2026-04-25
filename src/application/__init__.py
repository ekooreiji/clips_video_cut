"""
Application Layer - Camada de Aplicação
"""

from src.application.pipeline import VideoPipeline
from src.application.batch_processor import BatchProcessor

__all__ = ["VideoPipeline", "BatchProcessor"]