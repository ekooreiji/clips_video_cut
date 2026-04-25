"""
Validators - Validadores do Sistema
"""

from pathlib import Path
from typing import Optional

from src.common.exceptions import ConfigurationError


def validate_video_path(path: Path) -> bool:
    """
    Valida caminho de vídeo.
    
    Args:
        path: Caminho a validar
        
    Returns:
        True se válido
        
    Raises:
        ConfigurationError: Se caminho inválido
    """
    if not path:
        raise ConfigurationError("Caminho de vídeo vazio")
    
    if not path.exists():
        raise ConfigurationError(f"Arquivo não encontrado: {path}")
    
    valid_extensions = {'.mp4', '.mkv', '.avi', '.webm', '.mov'}
    
    if path.suffix.lower() not in valid_extensions:
        raise ConfigurationError(
            f"Formato não suportado: {path.suffix}. "
            f"Use: {', '.join(valid_extensions)}"
        )
    
    return True


def validate_config(config: dict) -> bool:
    """
    Valida configuração.
    
    Args:
        config: Dicionário de configuração
        
    Returns:
        True se válido
        
    Raises:
        ConfigurationError: Se configuração inválida
    """
    required_keys = ['processing', 'output']
    
    for key in required_keys:
        if key not in config:
            raise ConfigurationError(f"Chave ausente: {key}")
    
    # Validar thresholds
    if 'silence_removal' in config.get('processing', {}):
        sil = config['processing']['silence_removal']
        
        if sil.get('db_threshold', -40) > 0:
            raise ConfigurationError(
                "silence_removal.db_threshold deve ser negativo"
            )
        
        if sil.get('min_duration', 0.5) <= 0:
            raise ConfigurationError(
                "silence_removal.min_duration deve ser maior que 0"
            )
    
    return True


def validate_batch_directory(directory: Path, max_files: int = 10) -> int:
    """
    Valida diretório para batch processing.
    
    Args:
        directory: Diretório com vídeos
        max_files: Máximo de arquivos permitidos
        
    Returns:
        Número de vídeos encontrados
        
    Raises:
        ConfigurationError: Se diretório inválido
    """
    if not directory.exists():
        raise ConfigurationError(f"Diretório não encontrado: {directory}")
    
    if not directory.is_dir():
        raise ConfigurationError(f"Não é um diretório: {directory}")
    
    # Contar vídeos
    extensions = ['.mp4', '.mkv', '.avi', '.webm', '.mov']
    videos = []
    
    for ext in extensions:
        videos.extend(directory.glob(f"*{ext}"))
    
    if not videos:
        raise ConfigurationError(f"Nenhum vídeo encontrado em: {directory}")
    
    if len(videos) > max_files:
        raise ConfigurationError(
            f"Muitos vídeos ({len(videos)}). Máximo: {max_files}"
        )
    
    return len(videos)