"""
Logger - Sistema de Logging

Utilitário para configuração e acesso a logging.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str = "clips_videos",
    level: str = "INFO",
    log_file: Optional[Path] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Configura e retorna logger.
    
    Args:
        name: Nome do logger
        level: Nível de logging (DEBUG, INFO, WARNING, ERROR)
        log_file: Arquivo para output (opcional)
        format_string: Formato customizado (opcional)
        
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    
    # Evitar duplicatas
    if logger.handlers:
        return logger
    
    # Converter nível
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    logger.setLevel(level_map.get(level.upper(), logging.INFO))
    
    # Formato
    if format_string is None:
        format_string = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    
    formatter = logging.Formatter(format_string)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (se especificado)
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = "clips_videos") -> logging.Logger:
    """
    Obtém logger existente ou cria novo.
    
    Args:
        name: Nome do logger
        
    Returns:
        Logger
    """
    logger = logging.getLogger(name)
    
    # Se não tem handlers, configurar básico
    if not logger.handlers:
        return setup_logger(name)
    
    return logger