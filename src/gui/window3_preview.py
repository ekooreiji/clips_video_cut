"""
Window 3: Preview Interativo
Janela com 3 painéis: vídeos (esquerda), player (centro), clips (direita).
Sincronizado com CLI src.cli.commands.
"""
from pathlib import Path
from typing import List, Dict, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QListWidget, QListWidgetItem, QFrame,
    QSplitter, QProgressBar, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from src.application.pipeline import VideoPipeline
from src.domain.values.config import ProcessingConfig
from src.gui.video_player import VideoPlayerWidget
from src.common.utils.logger import setup_logger, get_logger

# Setup logger
setup_logger(level="INFO")
logger = get_logger(__name__)


class DetectThread(QThread):
    """Thread para detecção de clips (mesma lógica da CLI)."""
    progress = pyqtSignal(str, int)
    finished = pyqtSignal(str, list)
    error = pyqtSignal(str, str)

    def __init__(self, video_path: Path, config: ProcessingConfig):
        super().__init__()
        self.video_path = video_path
        self.config = config

    def run(self):
        try:
            logger.info(f"Detectando scene cuts em: {self.video_path.name}")
            self.progress.emit(str(self.video_path), 0)
            
            # Mesma lógica da CLI
            pipeline = VideoPipeline(config=self.config)
            result = pipeline.preview(self.video_path)
            
            clips = result.get('clips', [])
            logger.info(f"{len(clips)} clips detectados em {self.video_path.name}")
            
            self.finished.emit(str(self.video_path), clips)
        except Exception as e:
            logger.error(f"Erro detectando {self.video_path.name}: {e}")
            self.error.emit(str(self.video_path), str(e))


class PreviewWindow(QWidget):
    """Janela de preview com 3 painéis."""
    
    # Sinal para pedir processamento
    process_requested = pyqtSignal()  # Emitido quando clica em "Processar"

    def __init__(self, video_paths: List[Path], config: ProcessingConfig, 
                 detected_clips: Dict[str, list] = None, parent: QWidget = None):
        super().__init__(parent)
        self.video_paths = video_paths
        self.config = config
        self.detected_clips = detected_clips or {}
        self.workers: Dict[str, DetectThread] = {}
        self.init_ui()
        
        # Se não tinha clips, detecta agora
        if not self.detected_clips:
            self.auto_detect_all()
        else:
            # Já tem os clips, mostra na lista
            if self.video_paths:
                current = self.video_paths[0]
                if str(current) in self.detected_clips:
                    clips = self.detected_clips[str(current)]
                    self.update_clips_list(clips)
                    # Passar clips para o player
                    self.player.set_clips(clips)
                    # Habilitar botão de processar
                    if clips:
                        self.process_button.setEnabled(True)

    def init_ui(self):
        """Inicializa interface"""
        self.setWindowTitle("Video Clip Automation - Preview")
        self.setGeometry(100, 100, 1200, 700)
        
        layout = QHBoxLayout(self)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Painel esquerda: vídeos
        left_panel = self.create_video_panel()
        splitter.addWidget(left_panel)
        
        # Painel centro: player
        self.player = VideoPlayerWidget()
        splitter.addWidget(self.player)
        
        # Painel direita: clips
        right_panel = self.create_clips_panel()
        splitter.addWidget(right_panel)
        
        splitter.setSizes([220, 600, 320])
        
        layout.addWidget(splitter)
        
        # Botões inferiores
        bottom_layout = QHBoxLayout()
        
        back_button = QPushButton("← Fechar")
        back_button.clicked.connect(self.close)
        bottom_layout.addWidget(back_button)
        
        bottom_layout.addStretch()
        
        self.process_button = QPushButton("▶ Processar Selecionados")
        self.process_button.clicked.connect(self.process_selected)
        self.process_button.setEnabled(False)
        bottom_layout.addWidget(self.process_button)
        
        layout.addLayout(bottom_layout)

    def create_video_panel(self) -> QFrame:
        """Painel de vídeos"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        panel.setMinimumWidth(180)
        layout = QVBoxLayout(panel)
        
        header = QLabel("VÍDEOS")
        header.setStyleSheet("font-weight: bold;")
        layout.addWidget(header)
        
        self.video_list = QListWidget()
        self.video_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.video_list.itemClicked.connect(self.on_video_clicked)
        layout.addWidget(self.video_list)
        
        # Adicionar vídeos à lista
        for path in self.video_paths:
            item = QListWidgetItem(path.name)
            item.setData(Qt.ItemDataRole.UserRole, path)
            self.video_list.addItem(item)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        return panel

    def create_clips_panel(self) -> QFrame:
        """Painel de clips"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        panel.setMinimumWidth(260)
        layout = QVBoxLayout(panel)
        
        header = QLabel("CLIPS DETECTADOS")
        header.setStyleSheet("font-weight: bold;")
        layout.addWidget(header)
        
        self.clips_list = QListWidget()
        self.clips_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.clips_list.itemClicked.connect(self.on_clip_clicked)
        layout.addWidget(self.clips_list)
        
        info_label = QLabel("Clique num clip para reproduzir")
        info_label.setStyleSheet("color: gray; font-size: 11px;")
        layout.addWidget(info_label)
        
        return panel

    def auto_detect_all(self):
        """Auto-detecta clips para todos os vídeos (como CLI)."""
        logger.info(f"Iniciando detecção automática para {len(self.video_paths)} vídeo(s)")
        
        for path in self.video_paths:
            self.detect_clips_for_video(path)
    
    def detect_clips_for_video(self, video_path: Path):
        """Detecta clips para um vídeo (mesma lógica da CLI)."""
        if str(video_path) in self.workers:
            return
        
        self.progress_bar.setVisible(True)
        logger.info(f"Thread detectando: {video_path.name}")
        
        worker = DetectThread(video_path, self.config)
        worker.progress.connect(lambda vp, pct: self.on_progress(vp, pct))
        worker.finished.connect(lambda vp, clips: self.on_finished(Path(vp), clips))
        worker.error.connect(lambda vp, err: self.on_error(Path(vp), err))
        
        self.workers[str(video_path)] = worker
        worker.start()

    def on_progress(self, video_path: str, pct: int):
        """Progresso da detecção"""
        self.progress_bar.setFormat(f"Detectando: {Path(video_path).name}")

    def on_finished(self, video_path: Path, clips: list):
        """Detecção concluída"""
        self.detected_clips[str(video_path)] = clips
        
        if str(video_path) in self.workers:
            del self.workers[str(video_path)]
        
        self.progress_bar.setVisible(False)
        
        # Atualiza lista de clips se for o vídeo atual
        current = self.get_current_video()
        if video_path == current:
            self.update_clips_list(clips)
        
        self.process_button.setEnabled(True)
        logger.info(f"✓ {len(clips)} clips detectados em {video_path.name}")

    def on_error(self, video_path: Path, error: str):
        """Erro na detecção"""
        if str(video_path) in self.workers:
            del self.workers[str(video_path)]
        
        self.progress_bar.setVisible(False)
        logger.error(f"✗ Erro em {video_path.name}: {error}")
        
        QMessageBox.warning(self, "Erro", f"{video_path.name}: {error}")

    def on_video_clicked(self, item):
        """Clicou num vídeo"""
        path = item.data(Qt.ItemDataRole.UserRole)
        
        if path and str(path) in self.detected_clips:
            clips = self.detected_clips[str(path)]
            self.update_clips_list(clips)
            
            # Passar lista de clips para o player
            self.player.set_clips(clips)
            
            # Habilitar botão de processar
            if clips:
                self.process_button.setEnabled(True)

    def on_clip_clicked(self, item):
        """Clicou num clip"""
        data = item.data(Qt.ItemDataRole.UserRole)
        if data:
            video_path, clip = data
            
            # Passar lista de clips para o player
            current = self.get_current_video()
            if current and str(current) in self.detected_clips:
                self.player.set_clips(self.detected_clips[str(current)])
            
            self.player.load_clip(clip, video_path)
            
            # Garantir que botão de processar esteja ativo
            self.process_button.setEnabled(True)
    
    def update_clips_list(self, clips: list):
        """Atualiza lista de clips"""
        self.clips_list.clear()
        
        current = self.get_current_video()
        
        for clip in clips:
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, (current, clip))
            text = f"[{clip['id']}] {clip['start_time']:.2f}s - {clip['end_time']:.2f}s"
            item.setText(text)
            self.clips_list.addItem(item)

    def get_current_video(self) -> Optional[Path]:
        """Vídeo selecionado"""
        item = self.video_list.currentItem()
        if item:
            return item.data(Qt.ItemDataRole.UserRole)
        return self.video_paths[0] if self.video_paths else None

    def process_selected(self):
        """Processa clips - emite sinal para parent."""
        logger.info("Processando clips selecionados...")
        self.process_requested.emit()

    def closeEvent(self, event):
        """Fecha recursos"""
        for worker in self.workers.values():
            worker.quit()
            worker.wait()
        self.player.close()
        event.accept()
        self.deleteLater()