"""
Window 2: Configuração
Janela de configuração de parâmetros de processamento.
"""
from pathlib import Path
from typing import List, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QCheckBox, QSpinBox, QDoubleSpinBox,
    QComboBox, QGroupBox, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from src.domain.values.config import ProcessingConfig


class ConfigWindow(QWidget):
    """Janela de configuração."""
    
    # Sinais para navegar
    back_clicked = pyqtSignal()  # Volta para seleção
    preview_clicked = pyqtSignal(list, ProcessingConfig)  # Abre preview
    process_clicked = pyqtSignal(list, ProcessingConfig)  # Processa
    
    def __init__(self, video_paths: List[Path]):
        super().__init__()
        self.video_paths = video_paths
        self.config = ProcessingConfig()
        self.init_ui()
    
    def init_ui(self):
        """Inicializa interface"""
        self.setWindowTitle("Video Clips Automation - Configuração")
        self.setGeometry(150, 150, 700, 600)
        
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("Configuração de Processamento")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        # Info dos vídeos
        layout.addWidget(QLabel(f"{len(self.video_paths)} vídeo(s) selecionado(s)"))
        
        # Scroll para opções
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(400)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Opções de Corte Visual
        scroll_layout.addWidget(self.create_visual_options())
        
        # Opções de Áudio
        scroll_layout.addWidget(self.create_audio_options())
        
        # Opções de Legendas
        scroll_layout.addWidget(self.create_subtitles_options())
        
        # Opções de Saída
        scroll_layout.addWidget(self.create_output_options())
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        # Botões de navegação
        nav_buttons = QHBoxLayout()
        
        back_button = QPushButton("← Voltar")
        back_button.clicked.connect(self.go_back)
        nav_buttons.addWidget(back_button)
        
        nav_buttons.addStretch()
        
        preview_button = QPushButton("🔍 Preview Interativo")
        preview_button.clicked.connect(self.go_preview)
        nav_buttons.addWidget(preview_button)
        
        process_button = QPushButton("▶ Processar")
        process_button.setStyleSheet("font-weight: bold;")
        process_button.clicked.connect(self.go_process)
        nav_buttons.addWidget(process_button)
        
        layout.addLayout(nav_buttons)
    
    def create_visual_options(self) -> QGroupBox:
        """Opções de corte visual"""
        group = QGroupBox("Corte Visual")
        layout = QVBoxLayout()
        
        self.visual_cut_check = QCheckBox("Detectar mudanças de cena")
        self.visual_cut_check.setChecked(True)
        layout.addWidget(self.visual_cut_check)
        
        # Sensibilidade
        sens_layout = QHBoxLayout()
        sens_layout.addWidget(QLabel("Sensibilidade:"))
        self.sensitivity_combo = QComboBox()
        self.sensitivity_combo.addItems(["Baixa", "Média", "Alta"])
        self.sensitivity_combo.setCurrentText("Média")
        sens_layout.addWidget(self.sensitivity_combo)
        sens_layout.addStretch()
        layout.addLayout(sens_layout)
        
        # Scene Cut Threshold
        thresh_layout = QHBoxLayout()
        thresh_layout.addWidget(QLabel("Scene Cut Threshold:"))
        self.scene_threshold_spin = QDoubleSpinBox()
        self.scene_threshold_spin.setRange(0.0, 1.0)
        self.scene_threshold_spin.setSingleStep(0.1)
        self.scene_threshold_spin.setValue(0.5)
        self.scene_threshold_spin.setToolTip("0.8 = só cortes abruptos, 0.5 = padrão")
        thresh_layout.addWidget(self.scene_threshold_spin)
        thresh_layout.addStretch()
        layout.addLayout(thresh_layout)
        
        # Min Scene Frames
        frames_layout = QHBoxLayout()
        frames_layout.addWidget(QLabel("Mín. Frames por Cena:"))
        self.min_frames_spin = QSpinBox()
        self.min_frames_spin.setRange(1, 100)
        self.min_frames_spin.setValue(10)
        frames_layout.addWidget(self.min_frames_spin)
        frames_layout.addStretch()
        layout.addLayout(frames_layout)
        
        # Min Clip Duration
        duration_layout = QHBoxLayout()
        duration_layout.addWidget(QLabel("Mín. Duração Clip (s):"))
        self.min_duration_spin = QDoubleSpinBox()
        self.min_duration_spin.setRange(0.0, 60.0)
        self.min_duration_spin.setSingleStep(0.5)
        self.min_duration_spin.setValue(0.0)
        duration_layout.addWidget(self.min_duration_spin)
        duration_layout.addStretch()
        layout.addLayout(duration_layout)
        
        group.setLayout(layout)
        return group
    
    def create_audio_options(self) -> QGroupBox:
        """Opções de áudio"""
        group = QGroupBox("Áudio")
        layout = QVBoxLayout()
        
        # Remover silêncio
        self.silence_check = QCheckBox("Remover silêncio")
        self.silence_check.stateChanged.connect(self.silence_toggled)
        layout.addWidget(self.silence_check)
        
        # Threshold de silêncio
        db_layout = QHBoxLayout()
        db_layout.addWidget(QLabel("Threshold (dB):"))
        self.silence_db_spin = QSpinBox()
        self.silence_db_spin.setRange(-60, -10)
        self.silence_db_spin.setValue(-40)
        self.silence_db_spin.setEnabled(False)
        db_layout.addWidget(self.silence_db_spin)
        db_layout.addStretch()
        layout.addLayout(db_layout)
        
        # Normalizar
        self.normalize_check = QCheckBox("Normalizar volume")
        layout.addWidget(self.normalize_check)
        
        group.setLayout(layout)
        return group
    
    def create_subtitles_options(self) -> QGroupBox:
        """Opções de legendas"""
        group = QGroupBox("Legendas")
        layout = QVBoxLayout()
        
        # Gerar legendas
        self.subtitles_check = QCheckBox("Gerar legendas (Whisper)")
        self.subtitles_check.stateChanged.connect(self.subtitles_toggled)
        layout.addWidget(self.subtitles_check)
        
        # Modelo Whisper
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("Modelo:"))
        self.whisper_combo = QComboBox()
        self.whisper_combo.addItems(["tiny", "base", "small", "medium"])
        self.whisper_combo.setCurrentText("base")
        self.whisper_combo.setEnabled(False)
        model_layout.addWidget(self.whisper_combo)
        model_layout.addStretch()
        layout.addLayout(model_layout)
        
        # Burn subtitles
        self.burn_check = QCheckBox("Inserir no vídeo")
        self.burn_check.setEnabled(False)
        layout.addWidget(self.burn_check)
        
        group.setLayout(layout)
        return group
    
    def create_output_options(self) -> QGroupBox:
        """Opções de saída"""
        group = QGroupBox("Saída")
        layout = QVBoxLayout()
        
        # Opção de diretório de saída
        dir_label = QLabel("Pasta de saída:")
        layout.addWidget(dir_label)
        
        # Radio buttons para escolha
        same_folder_layout = QHBoxLayout()
        self.same_folder_radio = QCheckBox("Mesma pasta do vídeo")
        self.same_folder_radio.setChecked(True)
        self.same_folder_radio.stateChanged.connect(self.output_folder_toggled)
        same_folder_layout.addWidget(self.same_folder_radio)
        layout.addLayout(same_folder_layout)
        
        custom_folder_layout = QHBoxLayout()
        self.custom_folder_radio = QCheckBox("Pasta personalizada:")
        self.custom_folder_radio.stateChanged.connect(self.output_folder_toggled)
        custom_folder_layout.addWidget(self.custom_folder_radio)
        
        self.output_folder_line = QLabel("(nenhuma)")
        self.output_folder_line.setStyleSheet("color: gray;")
        custom_folder_layout.addWidget(self.output_folder_line)
        
        browse_button = QPushButton("...")
        browse_button.setMaximumWidth(30)
        browse_button.clicked.connect(self.browse_output_folder)
        custom_folder_layout.addWidget(browse_button)
        
        layout.addLayout(custom_folder_layout)
        
        self.output_folder_path = None  # Armazena o caminho customizado
        
        # Excluir original
        self.destroy_check = QCheckBox("Excluir arquivo original após processar")
        layout.addWidget(self.destroy_check)
        
        group.setLayout(layout)
        return group
    
    def output_folder_toggled(self, state):
        """Alterna entre pasta sama ou customizada"""
        # Se same_folder está marcada, desmarca custom
        if self.sender() == self.same_folder_radio:
            if state == Qt.CheckState.Checked.value:
                self.custom_folder_radio.setChecked(False)
        elif self.sender() == self.custom_folder_radio:
            if state == Qt.CheckState.Checked.value:
                self.same_folder_radio.setChecked(False)
    
    def browse_output_folder(self):
        """Abre diálogo para selecionar pasta"""
        from PyQt6.QtWidgets import QFileDialog
        folder = QFileDialog.getExistingDirectory(
            self,
            "Selecionar Pasta de Saída",
            ""
        )
        if folder:
            self.output_folder_path = Path(folder)
            self.output_folder_line.setText(folder)
            self.output_folder_line.setStyleSheet("color: black;")
            self.custom_folder_radio.setChecked(True)
    
    def silence_toggled(self, state):
        """Alterna opções de silêncio"""
        enabled = state == Qt.CheckState.Checked.value
        self.silence_db_spin.setEnabled(enabled)
    
    def subtitles_toggled(self, state):
        """Alterna opções de legendas"""
        enabled = state == Qt.CheckState.Checked.value
        self.whisper_combo.setEnabled(enabled)
        self.burn_check.setEnabled(enabled)
    
    def get_config(self) -> ProcessingConfig:
        """Retorna configuração atual"""
        sensitivity_map = {"Baixa": 0.3, "Média": 1.0, "Alta": 2.0}
        
        self.config.visual_cut.enabled = self.visual_cut_check.isChecked()
        self.config.visual_cut.sensitivity = sensitivity_map[self.sensitivity_combo.currentText()]
        self.config.visual_cut.scene_cut_threshold = self.scene_threshold_spin.value()
        self.config.visual_cut.min_scene_frames = self.min_frames_spin.value()
        self.config.visual_cut.min_clip_duration = self.min_duration_spin.value()
        
        self.config.silence.enabled = self.silence_check.isChecked()
        self.config.silence.db_threshold = self.silence_db_spin.value()
        
        self.config.normalization.enabled = self.normalize_check.isChecked()
        
        self.config.subtitles.enabled = self.subtitles_check.isChecked()
        self.config.subtitles.whisper_model = self.whisper_combo.currentText()
        self.config.subtitles.burn = self.burn_check.isChecked()
        
        self.config.output.keep_original = not self.destroy_check.isChecked()
        
        return self.config
    
    def get_output_dir(self) -> Optional[Path]:
        """Retorna pasta de saída configurada"""
        if self.custom_folder_radio.isChecked() and self.output_folder_path:
            return self.output_folder_path
        return None  # None = mesma pasta do vídeo
    
    def go_back(self):
        """Volta para seleção"""
        self.back_clicked.emit()
    
    def go_preview(self):
        """Abre preview interativo"""
        config = self.get_config()
        self.preview_clicked.emit(self.video_paths, config)
    
    def go_process(self):
        """Inicia processamento"""
        config = self.get_config()
        self.process_clicked.emit(self.video_paths, config)