"""
Preview Window - Janela de Preview Interativa
Janela com 3 painéis: vídeos (esquerda), player (centro), clips (direita).
"""
from pathlib import Path
from typing import Optional, List, Dict
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QListWidget, QListWidgetItem, QCheckBox,
    QSplitter, QFrame, QMessageBox, QProgressBar,
    QFileDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from src.application.pipeline import VideoPipeline
from src.domain.values.config import ProcessingConfig
from src.gui.video_player import VideoPlayerWidget
from src.common.utils.logger import get_logger

logger = get_logger(__name__)


class DetectThread(QThread):
    """Thread para detecção de clips em background."""
    progress = pyqtSignal(str, int)
    finished = pyqtSignal(str, list)
    error = pyqtSignal(str, str)

    def __init__(self, video_path: Path, config: ProcessingConfig):
        super().__init__()
        self.video_path = video_path
        self.config = config

    def run(self):
        try:
            self.progress.emit(f"Detectando em {self.video_path.name}...", 0)
            pipeline = VideoPipeline(config=self.config)
            result = pipeline.preview(self.video_path)
            self.finished.emit(str(self.video_path), result['clips'])
        except Exception as e:
            self.error.emit(str(self.video_path), str(e))


class PreviewWindow(QWidget):
    """Janela de preview com 3 painéis."""

    def __init__(self, config: ProcessingConfig = None):
        super().__init__()
        self.config = config or ProcessingConfig()
        self.video_paths: List[Path] = []
        self.detected_clips: Dict[str, list] = {}
        self.selected_clips: set = set()
        self.workers: Dict[str, DetectThread] = {}
        self.init_ui()

    def init_ui(self):
        """Inicializa interface"""
        self.setWindowTitle("Video Clip Automation - Preview")
        self.setGeometry(100, 100, 1200, 700)
        
        main_layout = QHBoxLayout(self)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        left_panel = self.create_video_panel()
        splitter.addWidget(left_panel)
        
        self.player = VideoPlayerWidget()
        splitter.addWidget(self.player)
        
        right_panel = self.create_clips_panel()
        splitter.addWidget(right_panel)
        
        splitter.setSizes([240, 600, 360])
        
        main_layout.addWidget(splitter)

    def create_video_panel(self) -> QFrame:
        """Cria painel de vídeos"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        panel.setMinimumWidth(200)
        layout = QVBoxLayout(panel)
        
        header = QLabel("VÍDEOS")
        header.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(header)
        
        self.video_list = QListWidget()
        self.video_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.video_list.itemClicked.connect(self.on_video_clicked)
        layout.addWidget(self.video_list)
        
        button_layout = QHBoxLayout()
        
        add_button = QPushButton("+ Adicionar")
        add_button.clicked.connect(self.add_videos)
        button_layout.addWidget(add_button)
        
        remove_button = QPushButton("- Remover")
        remove_button.clicked.connect(self.remove_videos)
        button_layout.addWidget(remove_button)
        
        layout.addLayout(button_layout)
        
        self.detect_button = QPushButton("Detectar Cortes")
        self.detect_button.clicked.connect(self.detect_clips)
        self.detect_button.setEnabled(False)
        layout.addWidget(self.detect_button)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        return panel

    def create_clips_panel(self) -> QFrame:
        """Cria painel de clips"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        panel.setMinimumWidth(280)
        layout = QVBoxLayout(panel)
        
        header = QLabel("CLIPS DETECTADOS")
        header.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(header)
        
        self.clips_list = QListWidget()
        self.clips_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.clips_list.itemClicked.connect(self.on_clip_clicked)
        layout.addWidget(self.clips_list)
        
        info_layout = QHBoxLayout()
        self.clip_info_label = QLabel("Nenhum clip selecionado")
        self.clip_info_label.setStyleSheet("color: gray; font-size: 11px;")
        info_layout.addWidget(self.clip_info_label)
        layout.addLayout(info_layout)
        
        process_layout = QHBoxLayout()
        
        self.process_selected_button = QPushButton("Processar Selecionados")
        self.process_selected_button.clicked.connect(self.process_selected)
        self.process_selected_button.setEnabled(False)
        process_layout.addWidget(self.process_selected_button)
        
        layout.addLayout(process_layout)
        
        return panel

    def add_videos(self):
        """Adiciona vídeos via diálogo"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Selecionar Vídeos",
            "",
            "Vídeos (*.mp4 *.mkv *.avi *.mov *.webm)"
        )
        
        for file_path in files:
            path = Path(file_path)
            if path not in self.video_paths:
                self.video_paths.append(path)
                item = QListWidgetItem(path.name)
                item.setData(Qt.ItemDataRole.UserRole, path)
                item.setCheckState(Qt.CheckState.Unchecked)
                self.video_list.addItem(item)
        
        self.detect_button.setEnabled(len(self.video_paths) > 0)

    def remove_videos(self):
        """Remove vídeos selecionados"""
        for item in self.video_list.selectedItems():
            path = item.data(Qt.ItemDataRole.UserRole)
            if path in self.video_paths:
                self.video_paths.remove(path)
            self.video_list.takeItem(self.video_list.row(item))
            
            if str(path) in self.detected_clips:
                del self.detected_clips[str(path)]
        
        self.detect_button.setEnabled(len(self.video_paths) > 0)

    def on_video_clicked(self, item):
        """Clicou num vídeo - detecta clips automaticamente"""
        path = item.data(Qt.ItemDataRole.UserRole)
        
        if path and str(path) not in self.detected_clips:
            self.detect_clips_for_video(path)

    def detect_clips_for_video(self, video_path: Path):
        """Detecta clips para um vídeo específico"""
        if video_path in self.workers:
            return
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        
        worker = DetectThread(video_path, self.config)
        worker.progress.connect(lambda msg, pct: self.update_progress(msg, pct))
        worker.finished.connect(lambda vp, clips: self.on_detection_finished(Path(vp), clips))
        worker.error.connect(lambda vp, err: self.on_detection_error(Path(vp), err))
        
        self.workers[video_path] = worker
        worker.start()

    def update_progress(self, message: str, percentage: int):
        """Atualiza progresso"""
        if percentage > 0:
            self.progress_bar.setValue(percentage)
        self.progress_bar.setFormat(message)

    def on_detection_finished(self, video_path: Path, clips: list):
        """Finalizou detecção"""
        self.detected_clips[str(video_path)] = clips
        
        if video_path in self.workers:
            del self.workers[video_path]
        
        self.progress_bar.setVisible(False)
        
        current_video = self.get_current_video()
        if video_path == current_video:
            self.update_clips_list(video_path, clips)
        
        logger.info(f"Detectados {len(clips)} clips em {video_path.name}")

    def on_detection_error(self, video_path: Path, error: str):
        """Erro na detecção"""
        if video_path in self.workers:
            del self.workers[video_path]
        
        self.progress_bar.setVisible(False)
        QMessageBox.warning(self, "Erro", f"Erro detectando {video_path.name}: {error}")

    def on_clip_clicked(self, item):
        """Clicou num clip - reproduz"""
        data = item.data(Qt.ItemDataRole.UserRole)
        if data:
            video_path, clip = data
            self.player.load_clip(clip, video_path)
            
            self.clip_info_label.setText(
                f"[{clip['id']}] {clip['start_time']:.2f}s - {clip['end_time']:.2f}s ({clip['reason']})"
            )

    def update_clips_list(self, video_path: Path, clips: list):
        """Atualiza lista de clips"""
        self.clips_list.clear()
        
        for clip in clips:
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, (video_path, clip))
            
            text = f"[{clip['id']}] {clip['start_time']:.2f}s - {clip['end_time']:.2f}s"
            item.setText(text)
            
            self.clips_list.addItem(item)

    def get_current_video(self) -> Optional[Path]:
        """Retorna vídeo selecionado atualmente"""
        current_item = self.video_list.currentItem()
        if current_item:
            return current_item.data(Qt.ItemDataRole.UserRole)
        return self.video_paths[0] if self.video_paths else None

    def detect_clips(self):
        """Detecta clips para todos os vídeos"""
        for video_path in self.video_paths:
            if str(video_path) not in self.detected_clips:
                self.detect_clips_for_video(video_path)
        
        if self.video_paths:
            current = self.get_current_video()
            if current and str(current) in self.detected_clips:
                self.update_clips_list(current, self.detected_clips[str(current)])

    def process_selected(self):
        """Processa clips selecionados"""
        if not self.selected_clips:
            QMessageBox.information(
                self, "Aviso", "Selecione pelo menos um clip para processar."
            )
            return
        
        QMessageBox.information(
            self, "Em desenvolvimento",
            "Processamento em lote será implementado em breve."
        )

    def closeEvent(self, event):
        """Fecha recursos"""
        for worker in self.workers.values():
            worker.quit()
            worker.wait()
        
        self.player.close()
        event.accept()