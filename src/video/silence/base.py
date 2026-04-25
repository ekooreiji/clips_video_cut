import cv2
import numpy as np
import subprocess
import os

# ==============================
# CONFIGURAÇÕES
# ==============================

VIDEO_PATH = "input.mp4"
OUTPUT_DIR = "output_clips"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SAMPLE_RATE = 2        # analisa a cada N frames
SMOOTH_WINDOW = 5      # suavização
MIN_CLIP_LENGTH = 10   # frames mínimos pra salvar


# ==============================
# 1. CALCULAR SCORES DE MOVIMENTO
# ==============================

def compute_motion_scores(video_path):
    cap = cv2.VideoCapture(video_path)

    ret, prev = cap.read()
    if not ret:
        return []

    scores = []
    frame_indices = []

    frame_id = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_id % SAMPLE_RATE == 0:
            diff = cv2.absdiff(prev, frame)
            score = np.mean(diff)

            scores.append(score)
            frame_indices.append(frame_id)

            prev = frame

        frame_id += 1

    cap.release()
    return scores, frame_indices


# ==============================
# 2. SUAVIZAR SCORES
# ==============================

def smooth(scores, window=5):
    return np.convolve(scores, np.ones(window)/window, mode='same')


# ==============================
# 3. DETECTAR CLIPS
# ==============================

def detect_clips(scores, frame_indices):
    scores = smooth(scores, SMOOTH_WINDOW)

    mean = np.mean(scores)
    threshold_low = mean * 0.5
    threshold_high = mean * 1.5

    clips = []
    in_clip = False

    for i in range(1, len(scores)):

        # início
        if not in_clip and scores[i] > threshold_high:
            start_frame = frame_indices[i]
            in_clip = True

        # fim
        elif in_clip and scores[i] < threshold_low:
            end_frame = frame_indices[i]

            if end_frame - start_frame > MIN_CLIP_LENGTH:
                clips.append((start_frame, end_frame))

            in_clip = False

    return clips


# ==============================
# 4. CONVERTER FRAME → TEMPO
# ==============================

def frame_to_time(frame, fps):
    return frame / fps


# ==============================
# 5. CORTAR COM FFMPEG
# ==============================

def cut_video(input_path, start_time, end_time, output_path):
    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-ss", str(start_time),
        "-to", str(end_time),
        "-c", "copy",
        output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# ==============================
# 6. PIPELINE PRINCIPAL
# ==============================

def process_video(video_path):
    print("📊 Calculando movimento...")
    scores, frame_indices = compute_motion_scores(video_path)

    print("✂️ Detectando clips...")
    clips = detect_clips(scores, frame_indices)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    print(f"🎬 {len(clips)} clips encontrados")

    for i, (start_f, end_f) in enumerate(clips):
        start_t = frame_to_time(start_f, fps)
        end_t = frame_to_time(end_f, fps)

        output = os.path.join(OUTPUT_DIR, f"clip_{i}.mp4")

        print(f"Salvando clip {i}: {start_t:.2f}s → {end_t:.2f}s")
        cut_video(video_path, start_t, end_t, output)


# ==============================
# EXECUTAR
# ==============================

if __name__ == "__main__":
    process_video(VIDEO_PATH)