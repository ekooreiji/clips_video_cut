"""
Dialogs - Diálogos da GUI

Diálogos para interação com o usuário.
"""

from pathlib import Path
from typing import Optional, List

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QDialogButtonBox,
    QCheckBox,
    QGroupBox,
)


class ClipSelectionDialog(QDialog):
    """
    Diálogo para seleção de clips.
    """
    
    def __init__(
        self,
        clips: List[dict],
        parent=None
    ):
        super().__init__(parent)
        
        self.clips = clips
        self.selected_clips = []
        
        self.init_ui()
    
    def init_ui(self):
        """Inicializa UI"""
        self.setWindowTitle("Selecionar Clips")
        self.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("Selecione os clips para processar:")
        layout.addWidget(title)
        
        # Lista de clips
        self.clip_list = QListWidget()
        
        for clip in self.clips:
            item = QListWidgetItem(
                f"Clip {clip['id']}: {clip['start_time']:.2f}s - {clip['end_time']:.2f}s ({clip['reason']})"
            )
            item.setCheckState(True)
            item.setData(1, clip)
            
            self.clip_list.addItem(item)
        
        layout.addWidget(self.clip_list)
        
        # Botões
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        layout.addWidget(buttons)
    
    def accept(self):
        """Handler de accept"""
        self.selected_clips = []
        
        for i in range(self.clip_list.count()):
            item = self.clip_list.item(i)
            if item.checkState():
                self.selected_clips.append(item.data(1))
        
        super().accept()


class ConfigDialog(QDialog):
    """
    Diálogo de configuração.
    """
    
    def __init__(self, config, parent=None):
        super().__init__(parent)
        
        self.config = config
        
        self.init_ui()
    
    def init_ui(self):
        """Inicializa UI"""
        self.setWindowTitle("Configurações")
        self.setMinimumSize(400, 300)
        
        layout = QVBoxLayout(self)
        
        # Grupo processamento
        proc_group = QGroupBox("Processamento")
        proc_layout = QVBoxLayout()
        
        self.visual_check = QCheckBox("Corte visual")
        self.visual_check.setChecked(self.config.visual_cut.enabled)
        proc_layout.addWidget(self.visual_check)
        
        self.silence_check = QCheckBox("Remover silêncio")
        self.silence_check.setChecked(self.config.silence.enabled)
        proc_layout.addWidget(self.silence_check)
        
        self.normalize_check = QCheckBox("Normalizar áudio")
        self.normalize_check.setChecked(self.config.normalization.enabled)
        proc_layout.addWidget(self.normalize_check)
        
        proc_group.setLayout(proc_layout)
        layout.addWidget(proc_group)
        
        # Grupo legendas
        subtitle_group = QGroupBox("Legendas")
        subtitle_layout = QVBoxLayout()
        
        self.subtitle_check = QCheckBox("Gerar legendas")
        self.subtitle_check.setChecked(self.config.subtitles.enabled)
        subtitle_layout.addWidget(self.subtitle_check)
        
        self.burn_check = QCheckBox("Inserir no vídeo")
        self.burn_check.setChecked(self.config.subtitles.burn)
        subtitle_layout.addWidget(self.burn_check)
        
        subtitle_group.setLayout(subtitle_layout)
        layout.addWidget(subtitle_group)
        
        # Botões
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.save_and_accept)
        buttons.rejected.connect(self.reject)
        
        layout.addWidget(buttons)
    
    def save_and_accept(self):
        """Salva e aceita"""
        self.config.visual_cut.enabled = self.visual_check.isChecked()
        self.config.silence.enabled = self.silence_check.isChecked()
        self.config.normalization.enabled = self.normalize_check.isChecked()
        self.config.subtitles.enabled = self.subtitle_check.isChecked()
        self.config.subtitles.burn = self.burn_check.isChecked()
        
        super().accept()


class AboutDialog(QDialog):
    """
    Diálogo sobre o aplicativo.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.init_ui()
    
    def init_ui(self):
        """Inicializa UI"""
        self.setWindowTitle("Sobre")
        self.setMinimumSize(300, 200)
        
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("Video Clips Automation")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        # Versão
        version = QLabel("Versão 1.0.0")
        layout.addWidget(version)
        
        # Descrição
        desc = QLabel(
            "Sistema CLI/GUI para automatizar\n"
            "cortes de vídeos baseado em\n"
            "detecção de mudança de cena"
        )
        layout.addWidget(desc)
        
        layout.addStretch()
        
        # Botão OK
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)