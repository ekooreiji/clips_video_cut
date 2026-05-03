"""
GUI - Interface Gráfica (PyQt6)
Sistema GUI para visualização e processamento de vídeos.
"""
from src.gui.gui_manager import GUIManager, main
from src.gui.window1_video_select import VideoSelectWindow
from src.gui.window2_config import ConfigWindow
from src.gui.window3_preview import PreviewWindow
from src.gui.window4_loading import LoadingWindow
from src.gui.window5_conclusion import ConclusionWindow
from src.gui.video_player import VideoPlayerWidget

__all__ = [
    "GUIManager",
    "VideoSelectWindow", 
    "ConfigWindow",
    "PreviewWindow",
    "LoadingWindow",
    "ConclusionWindow",
    "VideoPlayerWidget",
    "main"
]