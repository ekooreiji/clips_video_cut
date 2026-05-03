"""
GUI Manager - Gerenciador de Janelas
Gerencia o fluxo entre as janelas conforme Logica_gui.md.
Sincronizado com CLI src.cli.commands.
"""
from pathlib import Path
from typing import List, Optional
from PyQt6.QtWidgets import QApplication, QWidget
from src.domain.values.config import ProcessingConfig

# Importar janelas
from src.gui.window1_video_select import VideoSelectWindow
from src.gui.window2_config import ConfigWindow
from src.gui.window3_preview import PreviewWindow
from src.gui.window4_loading import LoadingWindow
from src.gui.window5_conclusion import ConclusionWindow
from src.gui.detect_loading import DetectLoadingWindow


class GUIManager:
    """
    Gerenciador de janelas conforme lógica definida:
    
    1. VideoSelectWindow - Seleção de vídeos
         ↓ Próximo
    2. ConfigWindow - Configuração
         ↓ Preview → 3. PreviewWindow
         ↓ Processar → 4. LoadingWindow → 5. ConclusionWindow → 1
    """
    
    def __init__(self):
        self.app = QApplication([])
        self.app.setStyle("Fusion")
        
        self.current_window: Optional[QWidget] = None
        self.video_paths: List[Path] = []
        self.config: Optional[ProcessingConfig] = None
    
    def start(self):
        """Inicia aplicação"""
        self.show_video_select()
        self.app.exec()
    
    def show_video_select(self):
        """Mostra janela de seleção de vídeos (Window 1)"""
        self.close_current()
        
        window = VideoSelectWindow()
        window.next_clicked.connect(self.on_videos_selected)
        window.show()
        self.current_window = window
    
    def show_config(self):
        """Mostra janela de configuração (Window 2)"""
        self.close_current()
        
        window = ConfigWindow(self.video_paths)
        window.back_clicked.connect(self.show_video_select)
        window.preview_clicked.connect(self.on_preview_clicked)
        window.process_clicked.connect(self.on_process_clicked)
        window.show()
        self.current_window = window
    
    def show_preview(self):
        """Mostra janela de loading de detecção primeiro"""
        # Primeiro mostra loading enquanto detecta
        self.loading_detect = DetectLoadingWindow(
            self.video_paths, 
            self.config
        )
        
        # Conectar sinal para quando detecção terminar
        self.loading_detect.detection_done.connect(self.on_detection_for_preview)
        
        self.loading_detect.show()
    
    def on_detection_for_preview(self, results: dict):
        """Após detecção, abre preview com clips detectados"""
        # Abre preview com os resultados
        window = PreviewWindow(
            self.video_paths, 
            self.config,
            detected_clips=results,
            parent=None
        )
        
        # Conectar sinal de processamento
        window.process_requested.connect(self.on_preview_process_clicked)
        
        window.show()
        self.preview_window = window
    
    def on_preview_process_clicked(self):
        """Clicou em Processar no preview"""
        # Pegar output_dir da janela de config se existir
        output_dir = None
        if hasattr(self, 'current_window') and self.current_window:
            if hasattr(self.current_window, 'get_output_dir'):
                output_dir = self.current_window.get_output_dir()
        
        # Fechar preview e abrir loading
        if hasattr(self, 'preview_window') and self.preview_window:
            self.preview_window.close()
        
        self.show_loading(output_dir)
    
    def show_loading(self, output_dir: Path = None):
        """Mostra janela de loading (Window 4)"""
        self.close_current()
        
        window = LoadingWindow(self.video_paths, self.config, output_dir)
        window.finished.connect(self.on_processing_finished)
        window.show()
        self.current_window = window
    
    def show_conclusion(self, results: dict):
        """Mostra janela de conclusão (Window 5)"""
        window = ConclusionWindow(results)
        window.restart.connect(self.on_restart)
        window.show()
        self.current_window = window
    
    def close_current(self):
        """Fecha janela atual"""
        if self.current_window:
            self.current_window.close()
            self.current_window = None
    
    # === handlers (mesma lógica da CLI) ===
    
    def on_videos_selected(self, video_paths: List[Path]):
        """Após selecionar vídeos"""
        self.video_paths = video_paths
        print(f"GUI: {len(video_paths)} vídeo(s) selecionado(s)")
        self.show_config()
    
    def on_preview_clicked(self, video_paths: List[Path], config: ProcessingConfig):
        """Clicou em Preview"""
        self.video_paths = video_paths
        self.config = config
        print(f"GUI: Abrindo preview para {len(video_paths)} vídeo(s)")
        self.show_preview()
    
    def on_process_clicked(self, video_paths: List[Path], config: ProcessingConfig):
        """Clicou em Processar"""
        self.video_paths = video_paths
        self.config = config
        print(f"GUI: Processando {len(video_paths)} vídeo(s) com config")
        
        # Pegar output_dir da janela de config
        output_dir = None
        if hasattr(self, 'current_window') and self.current_window:
            if hasattr(self.current_window, 'get_output_dir'):
                output_dir = self.current_window.get_output_dir()
        
        self.show_loading(output_dir)
    
    def on_preview_clicked(self, video_paths: List[Path], config: ProcessingConfig):
        """Clicou em Preview"""
        self.video_paths = video_paths
        self.config = config
        print(f"GUI: Abrindo preview para {len(video_paths)} vídeo(s)")
        self.show_preview()
    
    def on_processing_finished(self, results: dict):
        """Processamento concluído (mesma lógica da CLI)"""
        processed = len(results.get("processed", []))
        clips_total = results.get("clips_total", 0)
        print(f"GUI: Concluído - {processed} vídeos, {clips_total} clips")
        self.show_conclusion(results)
    
    def on_restart(self):
        """Reinicia aplicação"""
        self.close_current()
        print("GUI: Reiniciando...")
        self.show_video_select()


def main():
    """Ponto de entrada"""
    manager = GUIManager()
    manager.start()


if __name__ == "__main__":
    main()