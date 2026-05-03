"""
Window de Loading para Detecção
Janela de loading que mostra enquanto os clips são detectados.
"""
from pathlib import Path
from typing import List
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QProgressBar, QMessageBox
)
from PyQt6.QtCore import QThread, pyqtSignal


class DetectLoadingThread(QThread):
    """Thread para detecção em background."""
    progress = pyqtSignal(str, int)  # video_name, percentage
    finished = pyqtSignal(dict)  # {video_path: clips}
    error = pyqtSignal(str)

    def __init__(self, video_paths: List[Path], config):
        super().__init__()
        self.video_paths = video_paths
        self.config = config

    def run(self):
        from src.application.pipeline import VideoPipeline
        from src.common.utils.logger import get_logger
        logger = get_logger(__name__)
        
        try:
            results = {}
            total = len(self.video_paths)
            
            for i, video_path in enumerate(self.video_paths):
                self.progress.emit(video_path.name, int((i / total) * 100))
                
                logger.info(f"Detectando: {video_path.name}")
                
                pipeline = VideoPipeline(config=self.config)
                result = pipeline.preview(video_path)
                results[str(video_path)] = result.get('clips', [])
                
                logger.info(f"✓ {video_path.name}: {len(results[str(video_path)])} clips")
            
            self.finished.emit(results)
            
        except Exception as e:
            logger.error(f"Erro: {e}")
            self.error.emit(str(e))


class DetectLoadingWindow(QWidget):
    """Janela de loading para detecção."""
    
    detection_done = pyqtSignal(dict)  # Resultados da detecção
    
    def __init__(self, video_paths: List[Path], config, parent: QWidget = None):
        super().__init__(parent)
        self.video_paths = video_paths
        self.config = config
        self.results = {}
        self.init_ui()
    
    def init_ui(self):
        """Inicializa interface"""
        self.setWindowTitle("Detectando Clips...")
        self.setGeometry(300, 300, 400, 200)
        
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("Detectando Cortes...")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        # Info
        info = QLabel(f"Analisando {len(self.video_paths)} vídeo(s)...")
        layout.addWidget(info)
        
        # Progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Iniciando detecção...")
        layout.addWidget(self.status_label)
        
        # Iniciar
        self.start_detection()
    
    def start_detection(self):
        """Inicia detecção"""
        self.worker = DetectLoadingThread(self.video_paths, self.config)
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()
    
    def on_progress(self, video_name: str, pct: int):
        """Progresso"""
        self.progress_bar.setValue(pct)
        self.status_label.setText(f"Detectando: {video_name}")
    
    def on_finished(self, results: dict):
        """Detecção concluída"""
        self.results = results
        self.progress_bar.setValue(100)
        self.status_label.setText("✓ Detecção concluída!")
        
        # Emite sinal com resultados
        self.detection_done.emit(results)
        
        # Fecha a janela
        QThread.msleep(500)
        self.close()
    
    def on_error(self, error: str):
        """Erro"""
        self.status_label.setText(f"✕ Erro: {error}")
        QMessageBox.critical(self, "Erro", error)
        self.close()