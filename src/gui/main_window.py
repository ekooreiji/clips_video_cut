"""
Main Window - Janela Principal GUI
Interface gráfica principal usando PyQt6.
"""
from pathlib import Path
from typing import Optional
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QProgressBar, QCheckBox,
    QSpinBox, QDoubleSpinBox, QComboBox, QGroupBox, QTextEdit,
    QMessageBox,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from src.application.pipeline import VideoPipeline
from src.domain.values.config import ProcessingConfig
from src.gui.preview_window import PreviewWindow
from src.common.utils.logger import get_logger

logger = get_logger(__name__)


class BatchProcessingThread(QThread):
    """Thread para processamento em batch."""
    progress = pyqtSignal(str)
    video_progress = pyqtSignal(str, int, int)  # video, current, total
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, video_paths: list, config: ProcessingConfig):
        super().__init__()
        self.video_paths = video_paths
        self.config = config

    def run(self):
        try:
            results = {"processed": [], "failed": []}
            
            for i, video_path in enumerate(self.video_paths):
                self.video_progress.emit(str(video_path), i + 1, len(self.video_paths))
                
                pipeline = VideoPipeline(config=self.config)
                result = pipeline.process_single(video_path)
                results["processed"].append(result)
            
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """Janela principal da aplicação GUI."""

    def __init__(self):
        super().__init__()
        self.video_paths: list[Path] = []
        self.config = ProcessingConfig()
        self.worker: Optional[BatchProcessingThread] = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Video Clips Automation")
        self.setGeometry(100, 100, 900, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Botões de modo
        mode_layout = QHBoxLayout()
        
        self.single_button = QPushButton("Modo Vídeo Único")
        self.single_button.clicked.connect(self.show_single_mode)
        mode_layout.addWidget(self.single_button)
        
        self.batch_button = QPushButton("Modo Batch (Múltiplos)")
        self.batch_button.clicked.connect(self.show_batch_mode)
        mode_layout.addWidget(self.batch_button)
        
        self.preview_button = QPushButton("🔍 Preview Interativo")
        self.preview_button.clicked.connect(self.open_preview_window)
        mode_layout.addWidget(self.preview_button)
        
        main_layout.addLayout(mode_layout)
        
        # Info
        self.info_label = QLabel("Selecione um modo acima para começar")
        self.info_label.setStyleSheet("color: gray; padding: 10px;")
        main_layout.addWidget(self.info_label)

    def show_single_mode(self):
        """Modo de vídeo único"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Selecionar Vídeo", "", "Vídeos (*.mp4 *.mkv *.avi *.mov *.webm)"
        )
        
        if file_path:
            self.video_paths = [Path(file_path)]
            self.info_label.setText(f"Vídeo selecionado: {Path(file_path).name}")
            self.run_single_process()

    def show_batch_mode(self):
        """Modo de múltiplos vídeos"""
        files, _ = QFileDialog.getOpenFileNames(
            self, "Selecionar Vídeos", "", "Vídeos (*.mp4 *.mkv *.avi *.mov *.webm)"
        )
        
        if files:
            self.video_paths = [Path(f) for f in files]
            self.info_label.setText(f"{len(self.video_paths)} vídeos selecionados")
            self.run_batch_process()

    def open_preview_window(self):
        """Abre janela de preview interativo"""
        window = PreviewWindow(config=self.config)
        window.show()

    def run_single_process(self):
        """Executa processamento único"""
        if not self.video_paths:
            return
        
        self.config = self.get_config_from_ui()
        
        try:
            pipeline = VideoPipeline(config=self.config)
            result = pipeline.process_single(self.video_paths[0])
            QMessageBox.information(
                self, "Sucesso", 
                f"{result['clips_detected']} clips gerados!"
            )
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def run_batch_process(self):
        """Executa processamento em lote"""
        if not self.video_paths:
            return
        
        self.config = self.get_config_from_ui()
        
        self.batch_button.setEnabled(False)
        self.preview_button.setEnabled(False)
        
        self.worker = BatchProcessingThread(self.video_paths, self.config)
        self.worker.video_progress.connect(self.on_batch_progress)
        self.worker.finished.connect(self.on_batch_finished)
        self.worker.error.connect(self.on_batch_error)
        self.worker.start()

    def get_config_from_ui(self) -> ProcessingConfig:
        """Retorna configuração atual"""
        sensitivity_map = {"Baixa": 0.3, "Média": 1.0, "Alta": 2.0}
        
        # Para simplificar, retorna config padrão
        # Em implementação completa, pegaria valores da UI
        return self.config

    def on_batch_progress(self, video: str, current: int, total: int):
        """Progresso do batch"""
        self.info_label.setText(f"Processando {current}/{total}: {Path(video).name}")

    def on_batch_finished(self, results: dict):
        """Batch finalizado"""
        processed = len(results.get("processed", []))
        self.info_label.setText(f"{processed} vídeos processados")
        self.batch_button.setEnabled(True)
        self.preview_button.setEnabled(True)
        
        QMessageBox.information(
            self, "Sucesso", f"{processed} vídeos processados com sucesso!"
        )

    def on_batch_error(self, error: str):
        """Erro no batch"""
        QMessageBox.critical(self, "Erro", error)
        self.batch_button.setEnabled(True)
        self.preview_button.setEnabled(True)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())