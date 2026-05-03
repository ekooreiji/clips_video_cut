"""
Window 5: Conclusão
Janela de conclusão após processamento.
"""
from pathlib import Path
from typing import List, Dict
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QListWidget, QListWidgetItem, QFrame
)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QColor


class ConclusionWindow(QWidget):
    """Janela de conclusão."""
    
    restart = pyqtSignal()  # Para reiniciar
    
    def __init__(self, results: Dict, parent: QWidget = None):
        super().__init__(parent)
        self.results = results
        self.init_ui()
    
    def init_ui(self):
        """Inicializa interface"""
        self.setWindowTitle("Concluído")
        self.setGeometry(200, 200, 500, 400)
        
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("✓ Processamento Concluído!")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: green;")
        layout.addWidget(title)
        
        # Resumo
        processed = self.results.get("processed", [])
        failed = self.results.get("failed", [])
        
        summary = QLabel(f"{len(processed)} vídeo(s) processado(s)")
        layout.addWidget(summary)
        
        if failed:
            layout.addWidget(QLabel(f"{len(failed)} erro(s)"))
        
        # Lista de resultados
        layout.addWidget(QLabel("Resultados:"))
        
        self.results_list = QListWidget()
        layout.addWidget(self.results_list)
        
        for result in processed:
            clips = result.get("clips_detected", 0)
            video = Path(result.get("video_path", "")).name
            item = QListWidgetItem(f"✓ {video}: {clips} clip(s)")
            item.setForeground(QColor("green"))
            self.results_list.addItem(item)
        
        for error in failed:
            item = QListWidgetItem(f"✗ {error}")
            item.setForeground(QColor("red"))
            self.results_list.addItem(item)
        
        # Botão Novo Proces
        new_button = QPushButton("+ Novo Processamento")
        new_button.clicked.connect(self.restart)
        layout.addWidget(new_button)
        
        # Botão Fechar
        close_button = QPushButton("Fechar")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
    
    def closeEvent(self, event):
        """Ao fechar, emite sinal para reiniciar"""
        self.restart.emit()
        event.accept()
        self.deleteLater()