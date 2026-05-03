"""
Window 4: Loading
Janela de loading com progresso durante processamento.
Sincronizado com CLI src.cli.commands.
"""
from pathlib import Path
from typing import List
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QListWidget, QListWidgetItem, QProgressBar,
    QMessageBox
)
from PyQt6.QtCore import QThread, pyqtSignal
from src.application.pipeline import VideoPipeline
from src.common.utils.logger import setup_logger, get_logger

# Setup logger para GUI
setup_logger(level="INFO")
logger = get_logger(__name__)


class ProcessThread(QThread):
    """Thread para processamento em lote (mesmo lógica da CLI)."""
    progress = pyqtSignal(str, int, int)  # video, current, total
    finished = pyqtSignal(dict)  # results
    error = pyqtSignal(str)

    def __init__(self, video_paths: List[Path], config, output_dir: Path = None):
        super().__init__()
        self.video_paths = video_paths
        self.config = config
        self.output_dir = output_dir  # None = mesma pasta do vídeo

    def run(self):
        try:
            results = {"processed": [], "failed": [], "clips_total": 0}
            
            logger.info(f"Iniciando processamento de {len(self.video_paths)} vídeo(s)")
            
            for i, video_path in enumerate(self.video_paths):
                self.progress.emit(str(video_path), i + 1, len(self.video_paths))
                
                logger.info(f"Processando: {video_path.name}")
                
                # Mesma lógica da CLI (com output_dir)
                pipeline = VideoPipeline(config=self.config)
                result = pipeline.process_single(video_path, self.output_dir)
                
                results["processed"].append(result)
                results["clips_total"] += result.get("clips_detected", 0)
                
                logger.info(f"✓ {video_path.name}: {result.get('clips_detected', 0)} clips")
            
            logger.info(f"Concluído: {results['clips_total']} clips totais")
            self.finished.emit(results)
            
        except Exception as e:
            logger.error(f"Erro no processamento: {e}")
            self.error.emit(str(e))


class LoadingWindow(QWidget):
    """Janela de loading."""
    
    finished = pyqtSignal(dict)  # Resultados
    
    def __init__(self, video_paths: List[Path], config, output_dir: Path = None, parent: QWidget = None):
        super().__init__(parent)
        self.video_paths = video_paths
        self.config = config
        self.output_dir = output_dir  # None = mesma pasta
        self.total = len(video_paths)
        self.init_ui()
    
    def init_ui(self):
        """Inicializa interface"""
        self.setWindowTitle("Processando...")
        self.setGeometry(200, 200, 500, 400)
        
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("Processando Vídeos")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        # Progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(self.total)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Iniciando...")
        layout.addWidget(self.status_label)
        
        # Lista de vídeos
        layout.addWidget(QLabel("Vídeos processados:"))
        
        self.video_list = QListWidget()
        layout.addWidget(self.video_list)
        
        # Adicionar todos os vídeos à lista
        for path in self.video_paths:
            item = QListWidgetItem(path.name)
            item.setData(256, "pending")  # status: pending/done/error
            self.video_list.addItem(item)
        
        # Botão Cancelar
        cancel_button = QPushButton("✕ Cancelar")
        cancel_button.clicked.connect(self.cancel)
        layout.addWidget(cancel_button)
        
        # Iniciar processamento
        self.start_processing()
    
    def start_processing(self):
        """Inicia processamento (mesma lógica da CLI)."""
        logger.info("Iniciando thread de processamento")
        
        self.worker = ProcessThread(self.video_paths, self.config, self.output_dir)
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()
    
    def on_progress(self, video_path: str, current: int, total: int):
        """Progresso"""
        self.progress_bar.setValue(current)
        
        # Atualiza status do vídeo na lista
        video_name = Path(video_path).name
        for i in range(self.video_list.count()):
            item = self.video_list.item(i)
            if item.text() == video_name:
                item.setData(256, "processing")
                break
        
        self.status_label.setText(f"Processando ({current}/{total}): {video_name}")
        logger.info(f"Progresso: {current}/{total} - {video_name}")
    
    def on_finished(self, results: dict):
        """Processamento concluído"""
        # Atualiza todos os itens como done
        for i in range(self.video_list.count()):
            item = self.video_list.item(i)
            item.setData(256, "done")
        
        processed = len(results.get("processed", []))
        clips_total = results.get("clips_total", 0)
        
        self.status_label.setText(f"✓ Concluído: {processed} vídeos, {clips_total} clips")
        logger.info(f"Concluído: {processed} vídeos, {clips_total} clips")
        
        self.finished.emit(results)
        
        # Fecha após 1 segundo
        QThread.msleep(1000)
        self.close()
    
    def on_error(self, error: str):
        """Erro"""
        self.status_label.setText(f"✕ Erro: {error}")
        logger.error(f"Erro: {error}")
        
        QMessageBox.critical(self, "Erro", error)
    
    def cancel(self):
        """Cancela processamento"""
        if hasattr(self, 'worker'):
            logger.info("Cancelando processamento")
            self.worker.quit()
            self.worker.wait()
        
        self.close()