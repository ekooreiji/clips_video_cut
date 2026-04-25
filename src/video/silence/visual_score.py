import cv2
import numpy as np
from pathlib import Path

from src.common.exceptions.video.exceptions_video import VideoProcessingError, VideoNotFoundError


def check_video_existe(video_path):
    
    """
    Checa se o video existe, caso não exista retorna um erro

    Raises:
        VideoNotFoundError: indica que o video não foi encontrado no caminho especificado,
        isso pode ocorrer por diversos fatores, como um caminho de arquivo incorreto, 
        um arquivo movido ou excluído, ou problemas de permissão de acesso.
    """
    
    if not Path(video_path).exists():
        raise VideoNotFoundError(
            f"O vídeo não foi encontrado no caminho especificado: {video_path}"
        )


def check_video_is_valid(video):
    
    """
    Checa se o video pode ser lido, caso não retorna um erro

    Raises:
        VideoProcessingError: indica que o video não pode ser lido ou processado,
        isso pode ocorrer por diversos fatores, como um formato de video não
        suportado, um arquivo corrompido, ou problemas de codec.
    """
    
    video.set(cv2.CAP_PROP_POS_FRAMES, 0)
    is_readable, _ = video.read()
    if not is_readable:
        raise VideoProcessingError(
            "O vídeo não pode ser lido ou processado", video.get(cv2.CAP_PROP_FILENAME)
        )
    

def calculate_diference_frame_score(previous_frame, current_frame):
    
    """
    Calcula a diferença visual entre dois frames distintos, e aplica um calculo 
    matemático em cima da diferença
    
    Args:
        previous_frame (numpy.ndarray): Frame anterior do video
        current_frame (numpy.ndarray): Frame atual do video

    Returns:
        float: Score de diferença entre os frames, onde um valor baixo indica pouca
        variação visual entre os frames, assim como um valor alto indica muita 
        variação visual entre os frames.
    """
    
    
    diff = cv2.absdiff(previous_frame, current_frame)
    score = np.mean(diff)
    return score

def video_interaction_visual_score(video, sample_rate):
    
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    video.set(cv2.CAP_PROP_POS_FRAMES, 0)
    _, previous_frame = video.read()
    
    scores = {}
    
    for index_frame in range(
        sample_rate, total_frames, sample_rate
    ):
        video.set(cv2.CAP_PROP_POS_FRAMES, index_frame)
        
        is_readable, frame = video.read()
        if not is_readable:
            raise VideoProcessingError(
                "O vídeo não pode ser lido ou processado",
                video.get(cv2.CAP_PROP_FILENAME)
            )
        
        score = calculate_diference_frame_score(
            previous_frame, frame
        )
        
        scores[index_frame] = score
        previous_frame = frame
                
    return scores


def visual_silence_score(video_path, sample_rate=5):
    
    """
    Lê um video a apartir de uma analise dos frames, calcula a variavação entre os frames
    para determinar um score de silencio visual, onde um score baixo indica pouco variação,
    de movimento na cena 
    
    Args:
        video_path (Path): Caminho para o arquivo de video a ser processado.add()
        sample_rete (int, opcional): contagem de frames para amostragem, Padrão é avaliação é 
        de 5 em 5 frames por vez
    
    Returns:
        'float': Score de silencio visual, onde um valor baixo, indica pouca movimentação 
        entre  as cenas
    """
    
    check_video_existe(video_path)
    
    cap = cv2.VideoCapture(video_path)
    
    check_video_is_valid(cap)
    scores = video_interaction_visual_score(
        cap, sample_rate
    )
    cap.release()
    
    return scores


def calculate_average_silence_score(scores):
    
    """
    Calcula a média dos scores de silencio visual, onde um valor baixo indica pouca 
    movimentação entre as cenas, e um valor alto indica muita movimentação entre as cenas
    
    Args:
        scores (dict): Dicionário contendo os scores de silencio visual para cada frame 
        amostrado, onde a chave é o número do frame e o valor é o score de silencio
        visual para aquele frame.
        
    Returnss:
        float: Media dos scores de silencio visual, onde um valor baixo indica pouca
        movimentação entre as cenas, e um valor alto indica muita movimentação entre
        as class Computer:
    """
    
    return np.mean(list(scores.values()))

if __name__ == "__main__":
    video_path = Path(r"src\video\input\InShot_20241203_081955892.mp4")
    silence_score = visual_silence_score(video_path)
    print(f"Silence Score: {silence_score}")
    print(f"Average Silence Score: {calculate_average_silence_score(silence_score)}")