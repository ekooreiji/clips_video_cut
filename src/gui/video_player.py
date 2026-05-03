"""
Video Player Widget
Widget para reprodução de vídeo com controles.
Mostra apenas o clip selecionado.
"""
from pathlib import Path
from typing import Optional, List
import cv2
import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QSlider, QFrame
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage


class VideoPlayerWidget(QWidget):
    """Widget para reprodução de vídeo."""
    
    clip_selected = pyqtSignal(str)  # Emite ID do clip selecionado
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.current_video_path: Optional[Path] = None
        self.current_clip: Optional[dict] = None
        self.all_clips: List[dict] = []  # Lista de todos os clips
        self.current_clip_index: int = -1  # Índice do clip atual
        self.capture = None
        self.isPlaying = False
        self.init_ui()
    
    def init_ui(self):
        """Inicializa interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Frame do vídeo
        self.video_frame = QFrame()
        self.video_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        self.video_frame.setMinimumSize(640, 360)
        self.video_frame.setStyleSheet("background-color: black;")
        frame_layout = QVBoxLayout(self.video_frame)
        
        self.video_label = QLabel("Selecione um clip para visualizar")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet("color: gray; font-size: 16px;")
        frame_layout.addWidget(self.video_label)
        
        layout.addWidget(self.video_frame)
        
        # Controles
        controls_layout = QHBoxLayout()
        
        self.play_button = QPushButton("▶ Reproduzir")
        self.play_button.clicked.connect(self.toggle_play)
        self.play_button.setEnabled(False)
        controls_layout.addWidget(self.play_button)
        
        self.prev_button = QPushButton("◀ Anterior")
        self.prev_button.clicked.connect(self.previous_clip)
        self.prev_button.setEnabled(False)
        controls_layout.addWidget(self.prev_button)
        
        self.next_button = QPushButton("Próximo ▶")
        self.next_button.clicked.connect(self.next_clip)
        self.next_button.setEnabled(False)
        controls_layout.addWidget(self.next_button)
        
        layout.addLayout(controls_layout)
        
        # Tempo
        self.time_label = QLabel("--:-- / --:--")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.time_label)
        
        # Slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setEnabled(False)
        self.slider.sliderMoved.connect(self.on_slider_moved)
        layout.addWidget(self.slider)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
    
    def set_clips(self, clips: List[dict]):
        """Define a lista de clips"""
        self.all_clips = clips
        self.current_clip_index = -1
    
    def load_video(self, video_path: Path):
        """Carrega vídeo para reprodução"""
        self.current_video_path = video_path
        self.capture = cv2.VideoCapture(str(video_path))
        
        if self.capture.isOpened():
            self.fps = self.capture.get(cv2.CAP_PROP_FPS)
            self.total_frames = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
            self.duration = self.total_frames / self.fps if self.fps > 0 else 0
            
            self.play_button.setEnabled(True)
            self.slider.setEnabled(True)
            self.slider.setMaximum(self.total_frames - 1)
            
            # Primeiro frame
            self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.capture.read()
            if ret:
                self.display_frame(frame)
            
            self.time_label.setText(f"00:00 / {self.format_time(self.duration)}")
        else:
            self.video_label.setText("Erro ao carregar vídeo")
    
    def load_clip(self, clip: dict, video_path: Path):
        """Carrega um clip específico"""
        self.current_clip = clip
        self.current_video_path = video_path
        
        # Encontrar índice do clip na lista
        for i, c in enumerate(self.all_clips):
            if c.get('id') == clip.get('id'):
                self.current_clip_index = i
                break
        
        self.load_video(video_path)
        
        # Posicionar no INÍCIO do clip
        start_time = clip['start_time']
        start_frame = int(start_time * self.fps)
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        # Mostrar apenas o primeiro frame (não reproduzir automaticamente)
        ret, frame = self.capture.read()
        if ret:
            self.display_frame(frame)
        
        # Atualizar slider e tempo
        self.slider.setValue(start_frame)
        self.time_label.setText(
            f"{self.format_time(start_time)} / {self.format_time(clip['end_time'])}"
        )
        
        # Habilitar botões Anterior/Próximo
        if len(self.all_clips) > 1:
            self.prev_button.setEnabled(True)
            self.next_button.setEnabled(True)
        else:
            self.prev_button.setEnabled(False)
            self.next_button.setEnabled(False)
    
    def toggle_play(self):
        """Alterna reprodução"""
        if self.isPlaying:
            self.pause()
        else:
            self.play()
    
    def play(self):
        """Inicia reprodução"""
        if self.capture and self.current_clip:
            self.isPlaying = True
            self.play_button.setText("⏸ Pausar")
            
            # Iniciar timer
            self.timer.start(int(1000 / self.fps))
    
    def pause(self):
        """Pausa reprodução"""
        self.isPlaying = False
        self.play_button.setText("▶ Reproduzir")
        self.timer.stop()
    
    def update_frame(self):
        """Atualiza frame"""
        if not self.capture or not self.isPlaying:
            return
        
        ret, frame = self.capture.read()
        if ret:
            self.display_frame(frame)
            
            current_frame = int(self.capture.get(cv2.CAP_PROP_POS_FRAMES))
            current_time = current_frame / self.fps
            self.slider.setValue(current_frame)
            self.time_label.setText(
                f"{self.format_time(current_time)} / {self.format_time(self.current_clip['end_time'])}"
            )
            
            # Verificar se chegou ao fim do clip - PARAR e não continuar
            if current_time >= self.current_clip['end_time']:
                self.pause()
                # Voltar ao início do clip
                start_frame = int(self.current_clip['start_time'] * self.fps)
                self.capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        else:
            self.pause()
    
    def display_frame(self, frame):
        """Exibe frame"""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        q_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        
        # Redimensionar para caber
        scaled = pixmap.scaled(
            self.video_frame.size(), 
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.video_label.setPixmap(scaled)
        self.video_label.setText("")
    
    def format_time(self, seconds: float) -> str:
        """Formata tempo"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
    
    def previous_clip(self):
        """Vai para clip anterior (circular)"""
        if not self.all_clips or not self.current_video_path:
            return
        
        self.pause()
        
        # Circular: primeiro clip → último clip
        if self.current_clip_index <= 0:
            self.current_clip_index = len(self.all_clips) - 1
        else:
            self.current_clip_index -= 1
        
        # Carregar clip anterior
        clip = self.all_clips[self.current_clip_index]
        self.current_clip = clip
        self.load_clip(clip, self.current_video_path)
    
    def next_clip(self):
        """Vai para próximo clip (circular)"""
        if not self.all_clips or not self.current_video_path:
            return
        
        self.pause()
        
        # Circular: último clip → primeiro clip
        if self.current_clip_index >= len(self.all_clips) - 1:
            self.current_clip_index = 0
        else:
            self.current_clip_index += 1
        
        # Carregar próximo clip
        clip = self.all_clips[self.current_clip_index]
        self.current_clip = clip
        self.load_clip(clip, self.current_video_path)
    
    def on_slider_moved(self, position: int):
        """Quando usuário move o slider"""
        if self.capture:
            # Apenas permitir movimento dentro do clip
            if self.current_clip:
                start_frame = int(self.current_clip['start_time'] * self.fps)
                end_frame = int(self.current_clip['end_time'] * self.fps)
                
                if position < start_frame:
                    position = start_frame
                elif position > end_frame:
                    position = end_frame
                
                self.capture.set(cv2.CAP_PROP_POS_FRAMES, position)
                current_time = position / self.fps
                self.time_label.setText(
                    f"{self.format_time(current_time)} / {self.format_time(self.current_clip['end_time'])}"
                )
    
    def close(self):
        """Libera recursos"""
        if self.capture:
            self.capture.release()
        self.timer.stop()