"""
JSON Exporter - Exportador de Relatórios JSON
"""

from pathlib import Path
from typing import Dict, Any
import json


class JSONExporter:
    """Exportador de relatórios em formato JSON"""
    
    def export(self, data: Dict[str, Any], output_path: Path):
        """
        Exporta dados para JSON.
        
        Args:
            data: Dicionário com dados
            output_path: Arquivo de saída
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load(self, input_path: Path) -> Dict[str, Any]:
        """
        Carrega dados de JSON.
        
        Args:
            input_path: Arquivo de entrada
            
        Returns:
            Dicionário com dados
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            return json.load(f)