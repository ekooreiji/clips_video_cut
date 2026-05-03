"""
Window 1: Seleção de Vídeos
Primeira janela para selecionar múltiplos vídeos.
"""
from pathlib import Path
from typing import List, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QListWidget, QListWidgetItem, QFrame,
    QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal


class VideoSelectWindow(QWidget):
    """Janela de seleção de vídeos."""
    
    # Sinais para navegar entre janelas
    next_clicked = pyqtSignal(list)  # Lista de caminhos dos vídeos
    
    def __init__(self):
        super().__init__()
        self.video_paths: List[Path] = []
        self.init_ui()
    
    def init_ui(self):
        """Inicializa interface"""
        self.setWindowTitle("Video Clips Automation - Selecionar Vídeos")
        self.setGeometry(150, 150, 600, 500)
        
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("Selecione os Vídeos")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        # Instrução
        instruction = QLabel("Adicione um ou mais vídeos para processar")
        instruction.setStyleSheet("color: gray;")
        layout.addWidget(instruction)
        
        # Lista de vídeos
        self.video_list = QListWidget()
        self.video_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        layout.addWidget(self.video_list)
        
        # Botões
        buttons_layout = QHBoxLayout()
        
        add_button = QPushButton("+ Adicionar Vídeos")
        add_button.clicked.connect(self.add_videos)
        buttons_layout.addWidget(add_button)
        
        remove_button = QPushButton("- Remover Selecionados")
        remove_button.clicked.connect(self.remove_videos)
        buttons_layout.addWidget(remove_button)
        
        layout.addLayout(buttons_layout)
        
        # Info
        self.info_label = QLabel("Nenhum vídeo selecionado")
        self.info_label.setStyleSheet("color: gray; padding: 10px;")
        layout.addWidget(self.info_label)
        
        # Botão Próximo
        next_button = QPushButton("Próximo →")
        next_button.setStyleSheet("font-weight: bold; padding: 10px;")
        next_button.clicked.connect(self.go_next)
        next_button.setEnabled(False)
        self.next_button = next_button
        layout.addWidget(next_button)
    
    def add_videos(self):
        """Adiciona vídeos"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Selecionar Vídeos",
            "",
            "Vídeos (*.mp4 *.mkv *.avi *.mov *.webm)"
        )
        
        added_count = 0
        for file_path in files:
            path = Path(file_path)
            if path not in self.video_paths:
                self.video_paths.append(path)
                
                # Item com checkbox visual (texto marcado)
                item = QListWidgetItem(f"□ {path.name}")
                item.setData(Qt.ItemDataRole.UserRole, path)
                item.setToolTip(str(path))  # Caminho completo no tooltip
                
                self.video_list.addItem(item)
                added_count += 1
        
        self.update_info()
        
        if added_count > 0:
            QMessageBox.information(
                self, "Adicionados", 
                f"{added_count} vídeo(s) adicionado(s)"
            )
    
    def remove_videos(self):
        """Remove vídeos selecionados"""
        selected = self.video_list.selectedItems()
        
        if not selected:
            QMessageBox.warning(
                self, "Aviso", 
                "Selecione um vídeo para remover"
            )
            return
        
        # Remover na ordem inversa para não bagunçar índices
        rows = sorted([self.video_list.row(item) for item in selected], reverse=True)
        
        for row in rows:
            item = self.video_list.takeItem(row)
            path = item.data(Qt.ItemDataRole.UserRole)
            self.video_paths.remove(path)
        
        self.update_info()
    
    def update_info(self):
        """Atualiza informação"""
        count = len(self.video_paths)
        if count == 0:
            self.info_label.setText("Nenhum vídeo selecionado")
            self.next_button.setEnabled(False)
        else:
            self.info_label.setText(f"{count} vídeo(s) selecionado(s)")
            self.next_button.setEnabled(True)
    
    def go_next(self):
        """Vai para próxima janela"""
        if not self.video_paths:
            QMessageBox.warning(
                self, "Aviso", 
                "Selecione pelo menos um vídeo"
            )
            return
        
        self.next_clicked.emit(self.video_paths)