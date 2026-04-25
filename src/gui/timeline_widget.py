"""
Timeline Widget - Widget de Timeline para GUI

Widget para visualização e ajuste de pontos de corte.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
)
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QColor, QPen

from typing import List, Dict, Any, Optional


class TimelineWidget(QWidget):
    """
    Widget de timeline para visualização de pontos de corte.
    """
    
    def __init__(self, duration: float = 0.0):
        super().__init__()
        
        self.duration = duration
        self.clips: List[Dict[str, Any]] = []
        self.current_time: float = 0.0
        
        self.bg_color = QColor(45, 45, 45)
        self.timeline_color = QColor(80, 80, 80)
        self.clip_color = QColor(0, 180, 255)
        self.current_color = QColor(255, 50, 50)
        self.text_color = QColor(200, 200, 200)
        
        self.setMinimumHeight(80)
        self.setMinimumWidth(400)
    
    def set_duration(self, duration: float):
        """Define duração do vídeo"""
        self.duration = duration
        self.update()
    
    def set_clips(self, clips: List[Dict[str, Any]]):
        """Define clips para exibir"""
        self.clips = clips
        self.update()
    
    def set_current_time(self, time: float):
        """Define tempo atual"""
        self.current_time = time
        self.update()
    
    def paintEvent(self, event):
        """Desenha a timeline"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w = self.width()
        h = self.height()
        
        # Fundo
        painter.fillRect(0, 0, w, h, self.bg_color)
        
        if self.duration <= 0:
            return
        
        # Calculate positions
        scale = w / self.duration
        
        # Linha central
        center_y = h // 2
        painter.setPen(QPen(self.timeline_color, 2))
        painter.drawLine(20, center_y, w - 20, center_y)
        
        # Marcadores de tempo
        painter.setPen(QPen(self.text_color, 1))
        
        # Marcadores a cada 10%
        for i in range(0, 11):
            x = 20 + (w - 40) * i / 10
            time = self.duration * i / 10
            
            # Linha
            painter.drawLine(int(x), center_y - 5, int(x), center_y + 5)
            
            # Tempo
            painter.drawText(
                int(x) - 20,
                h - 10,
                f"{time:.1f}s"
            )
        
        # Clips
        painter.setPen(QPen(self.clip_color, 3))
        
        for clip in self.clips:
            start_x = 20 + clip['start_time'] * scale
            end_x = 20 + clip['end_time'] * scale
            
            painter.drawLine(
                int(start_x), center_y,
                int(end_x), center_y
            )
            
            # ID do clip
            painter.drawText(
                int(start_x) + 5,
                center_y - 10,
                f"C{clip['id']}"
            )
        
        # Posição atual
        if self.current_time > 0:
            current_x = 20 + self.current_time * scale
            painter.setPen(QPen(self.current_color, 2))
            painter.drawLine(int(current_x), 10, int(current_x), h - 10)
    
    def mousePressEvent(self, event):
        """Handler de clique"""
        if self.duration <= 0:
            return
        
        # Calcular tempo clicado
        w = self.width() - 40
        x = event.position().x() - 20
        
        if 0 <= x <= w:
            time = (x / w) * self.duration
            self.current_time = time
            self.update()
            
            # Emitir sinal
            self.clicked.emit(time)
    
    # Sinais
    from PyQt6.QtCore import pyqtSignal
    clicked = pyqtSignal(float)


class TimelineDockWidget(QWidget):
    """
    Widget dock com timeline e controles.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.duration = 0.0
        
        self.init_ui()
    
    def init_ui(self):
        """Inicializa UI"""
        layout = QVBoxLayout(self)
        
        # Timeline
        self.timeline = TimelineWidget()
        layout.addWidget(self.timeline)
        
        # Labels
        info_layout = QHBoxLayout()
        
        self.time_label = QLabel("00:00.0")
        self.duration_label = QLabel("/ 00:00.0")
        
        info_layout.addWidget(self.time_label)
        info_layout.addWidget(self.duration_label)
        info_layout.addStretch()
        
        layout.addLayout(info_layout)
    
    def set_duration(self, duration: float):
        """Define duração"""
        self.duration = duration
        self.timeline.set_duration(duration)
        
        mins = int(duration // 60)
        secs = duration % 60
        self.duration_label.setText(f"/ {mins:02d}:{secs:04.1f}")
    
    def set_clips(self, clips: List[Dict[str, Any]]):
        """Define clips"""
        self.timeline.set_clips(clips)
    
    def set_current_time(self, time: float):
        """Define tempo atual"""
        self.timeline.set_current_time(time)
        
        mins = int(time // 60)
        secs = time % 60
        self.time_label.setText(f"{mins:02d}:{secs:04.1f}")