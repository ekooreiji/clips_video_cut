"""
Preview Widget - Widget de Preview para GUI

Widget para visualização de frames e preview de vídeo.
"""

from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
)
from PyQt6.QtCore import Qt, pyqtSignal

import cv2
import numpy as np
from PyQt6.QtGui import QImage, QPixmap, QPainter, QColor


class PreviewWidget(QWidget):
    """
    Widget de preview de vídeo.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.video_path: Optional[Path] = None
        self.current_frame: Optional[np.ndarray] = None
        self.frame_size = (320, 180)
        
        self.init_ui()
    
    def init_ui(self):
        """Inicializa UI"""
        layout = QVBoxLayout(self)
        
        # Label do frame
        self.frame_label = QLabel()
        self.frame_label.setMinimumSize(*self.frame_size)
        self.frame_label.setMaximumSize(*self.frame_size)
        self.frame_label.setStyleSheet("background-color: black;")
        self.frame_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.frame_label)
        
        # Controles
        controls_layout = QHBoxLayout()
        
        self.prev_button = QPushButton("◀")
        self.prev_button.clicked.connect(self.prev_frame)
        
        self.play_button = QPushButton("▶")
        self.play_button.clicked.connect(self.toggle_play)
        
        self.next_button = QPushButton("▶")
        self.next_button.clicked.connect(self.next_frame)
        
        controls_layout.addWidget(self.prev_button)
        controls_layout.addWidget(self.play_button)
        controls_layout.addWidget(self.next_button)
        
        controls_layout.addStretch()
        
        # Frame info
        self.info_label = QLabel("Nenhum vídeo")
        
        layout.addWidget(self.info_label)
        layout.addLayout(controls_layout)
    
    def set_video(self, video_path: Path):
        """Define vídeo para preview"""
        self.video_path = video_path
        
        if video_path and video_path.exists():
            self.cap = cv2.VideoCapture(str(video_path))
            
            # Mostrar primeiro frame
            self.show_frame(0)
            
            # Info
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            self.info_label.setText(
                f"{video_path.name} | {fps:.1f} fps | {frame_count} frames"
            )
        else:
            self.info_label.setText("Vídeo não encontrado")
    
    def show_frame(self, frame_number: int):
        """Mostra frame específico"""
        if not self.video_path or not hasattr(self, 'cap'):
            return
        
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = self.cap.read()
        
        if ret:
            # Converter BGR para RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Redimensionar
            h, w, c = frame.shape
            ratio = self.frame_size[0] / w
            h_new = int(h * ratio)
            
            frame = cv2.resize(frame, (self.frame_size[0], h_new))
            
            # Converter para QPixmap
            img = QImage(
                frame.data,
                self.frame_size[0],
                h_new,
                self.frame_size[0] * 3,
                QImage.Format.Format_RGB888
            )
            
            pixmap = QPixmap.fromImage(img)
            
            self.frame_label.setPixmap(pixmap)
    
    def next_frame(self):
        """Próximo frame"""
        if hasattr(self, 'cap'):
            current = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
            self.show_frame(current + 1)
    
    def prev_frame(self):
        """Frame anterior"""
        if hasattr(self, 'cap'):
            current = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
            self.show_frame(max(0, current - 1))
    
    def toggle_play(self):
        """Play/Pause"""
        # Placeholder para implementação futura
        pass
    
    def closeEvent(self, event):
        """Fecha video capture"""
        if hasattr(self, 'cap'):
            self.cap.release()
        super().closeEvent(event)