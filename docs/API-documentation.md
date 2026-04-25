# Documentacao de API - Video Clips Automation

| Metadata | Valor |
|----------|-------|
| **Versao** | 1.0.0 |
| **Data** | 2026-04-24 |
| **Atualizado** | 2026-04-25 |

---

## Table of Contents

1. [Visao Geral](#1-visao-geral)
2. [Instalacao](#2-instalacao)
3. [Referencia Rapida](#3-referencia-rapida)
4. [CLI](#4-cli)
5. [Pipeline](#5-pipeline)
6. [Entidades](#6-entidades)
7. [Configuracao](#7-configuracao)
8. [Casos de Uso](#8-casos-de-uso)
9. [Adaptadores](#9-adaptadores)
10. [Exportadores](#10-exportadores)
11. [Excecoes](#11-excecoes)
12. [GUI](#12-gui)
13. [Exemplos](#13-exemplos)

---

## 1. Visao Geral

### 1.1 Introducao

A API do Video Clips Automation fornece interface programatica para processar videos automaticamente. Suporta deteccao de cena,_remocao de silencio, normalizacao de audio e geracao de legendas.

### 1.2 Caracteristicas

| Caracteristica | Descricao |
|----------------|-----------|
| **Deteccao de Cena** | Detecta mudancas visuais entre quadros |
| **Remocao de Silencio** | Remove regioes silenciosas do audio |
| **Normalizacao** | Normaliza volume do audio |
| **Legendas** | Gera legendas automaticamente |
| **Processamento em Lote** | Processa multiplos videos |

### 1.3 Instalacao

```bash
pip install clips-videos
```

Ou clone o repositorio:

```bash
git clone https://github.com/user/clips_videos.git
pip install -e clips_videos
```

---

## 2. Instalacao

### 2.1 Requisitos

- Python 3.10+
- FFmpeg (para processamento de video)

### 2.2 Dependencias

```
torch>=2.0.0
numpy>=1.24.0
opencv-python>=4.8.0
pydantic>=2.0.0
click>=8.1.0
PyQt6>=6.5.0
whisper>=20231101
imageio>=2.31.0
imageio-ffmpeg>=0.4.0
```

---

## 3. Referencia Rapida

### 3.1 Exemplo Basico

```python
from pathlib import Path
from src.application.pipeline import VideoPipeline
from src.domain.values.config import ProcessingConfig

# Configuracao padrao
config = ProcessingConfig()

# Pipeline
pipeline = VideoPipeline(config=config)

# Processar video
result = pipeline.process_single(Path("video.mp4"))

print(f"Clips detectados: {result['clips_detected']}")
print(f"Relatorio: {result['report_path']}")
```

### 3.2 Exemplo Completo

```python
from pathlib import Path
from src.application.pipeline import VideoPipeline
from src.domain.values.config import ProcessingConfig

# Configuracao personalizada
config = ProcessingConfig()
config.visual_cut.enabled = True
config.visual_cut.sensitivity = 1.2
config.silence.enabled = True
config.silence.db_threshold = -45
config.normalize_audio = True
config.subtitles.enabled = True
config.subtitles.format = "srt"

# Pipeline
pipeline = VideoPipeline(config=config, max_workers=2)

# Processar video
video_path = Path("video.mp4")
result = pipeline.process_single(video_path)

# Resultado
print(f"Status: {result['status']}")
print(f"Clips: {result['clips_detected']}")
print(f"Duracao total: {result['total_duration']}s")
print(f"Relatorio: {result['report_path']}")
```

---

## 4. CLI

### 4.1 Comando Process

Processa um ou varios videos.

```bash
python -m src.cli.commands process <caminho_video> [OPCOES]
```

#### Opciones

| Opcao | Tipo | Padrao | Descricao |
|-------|------|-------|------------|
| `--visual-cut` | bool | True | Ativar deteccao de cena |
| `--sensitivity` | str | medium | Sensibilidade (low/medium/high) |
| `--remove-silence` | bool | False | Remover silencio |
| `--silence-db` | int | -40 | Threshold dB |
| `--silence-duration` | float | 0.5 | Duracao minima |
| `--normalize-audio` | bool | False | Normalizar audio |
| `--generate-subtitles` | bool | False | Gerar legendas |
| `--export-subtitles` | str | srt | Formato (srt/vtt) |
| `--burn-subtitles` | bool | False | Inserir legendas |
| `--destroy` | bool | False | Excluir original |
| `--config` | Path | - | Arquivo JSON |
| `--batch` | Path | - | Pasta com videos |
| `-v, --verbose` | bool | False | Log verboso |

#### Ejemplos

```bash
# Processar com deteccao de cena
python -m src.cli.commands process video.mp4

# Processar com silencio removido
python -m src.cli.commands process video.mp4 --remove-silence

# Processar com tudo
python -m src.cli.commands process video.mp4 --visual-cut --remove-silence --normalize-audio --generate-subtitles

# Processar pasta
python -m src.cli.commands process video.mp4 --batch ./pasta
```

### 4.2 Comando Preview

Mostra os pontos de corte sem processar.

```bash
python -m src.cli.commands preview <caminho_video>
```

### 4.3 Comando Init Config

Cria arquivo de configurao.

```bash
python -m src.cli.commands init-config -o config.json
```

### 4.4 Comando GUI

Abre interface grafica.

```bash
python -m src.cli.commands gui
```

---

## 5. Pipeline

### 5.1 VideoPipeline

Orquestra todo o processo de processamento de video.

```python
class VideoPipeline:
    """Pipeline principal para processamento de videos"""

    def __init__(
        self,
        config: ProcessingConfig | None = None,
        max_workers: int = 3,
    ) -> None:
        """Inicializa o pipeline.

        Args:
            config: Configuracao de processamento.
            max_workers: Numero maximo de workers.

        Raises:
            ValueError: Se max_workers for invalido.
        """
        ...

    def process_single(self, video_path: Path) -> dict[str, Any]:
        """Processa um unico video.

        Args:
            video_path: Caminho para o video.

        Returns:
            Dicionario com resultado.

        Raises:
            FileNotFoundError: Se o video nao existir.
            ValueError: Se o video nao puder ser processado.
        """
        ...

    def process_batch(
        self,
        video_paths: list[Path],
    ) -> list[dict[str, Any]]:
        """Processa multiplos videos.

        Args:
            video_paths: Lista de caminhos de videos.

        Returns:
            Lista de resultados.
        """
        ...
```

#### Metodos

| Metodo | Descricao | Retorno |
|--------|-----------|---------|
| `process_single` | Processa um video | dict |
| `process_batch` | Processa varios videos | list[dict] |
| `get_metadata` | Obtem metadados do video | VideoDocument |

#### Exemplo

```python
from pathlib import Path
from src.application.pipeline import VideoPipeline
from src.domain.values.config import ProcessingConfig

config = ProcessingConfig(
    visual_cut={"enabled": True, "sensitivity": 1.0},
    silence={"enabled": True, "db_threshold": -40},
)

pipeline = VideoPipeline(config=config)

// Processar um video
result = pipeline.process_single(Path("video.mp4"))
print(f"Clips: {result['clips_detected']}")

// Processar varios
results = pipeline.process_batch([
    Path("video1.mp4"),
    Path("video2.mp4"),
])
```

---

## 6. Entidades

### 6.1 VideoDocument

Representa um video com seus metadados.

```python
class VideoDocument:
    """Entidade que representa um documento de video"""

    video_path: Path
    """Caminho do arquivo de video"""

    duration: float
    """Duracao em segundos"""

    fps: float
    """Quadros por segundo"""

    width: int
    """Largura do video"""

    height: int
    """Altura do video"""

    codec: str
    """Codec de video"""

    audio_codec: str | None
    """Codec de audio"""

    bitrate: int | None
    """Taxa de bits"""

    metadata: dict[str, Any]
    """Metadados extras"""
```

#### Criacao

```python
from pathlib import Path
from src.domain.entities.video import VideoDocument

video = VideoDocument(
    video_path=Path("video.mp4"),
    duration=120.5,
    fps=30.0,
    width=1920,
    height=1080,
    codec="h264",
    audio_codec="aac",
)
```

### 6.2 ClipSegment

Representa um segmento de clip.

```python
class ClipSegment:
    """Entidade que representa um segmento de clip"""

    video_path: Path
    """Caminho do video original"""

    start: float
    """Tempo de inicio em segundos"""

    end: float
    """Tempo de fim em segundos"""

    scene_index: int | None = None
    """Indice da cena"""

    silence_detected: bool = False
    """Se houve silencio detectado"""

    score: float | None = None
    """Score de confianca"""
```

#### Propriedades Calculadas

| Propriedade | Tipo | Descricao |
|------------|------|------------|
| `duration` | float | Duracao do clip |
| `timestamp_start` | Timestamp | Objeto Timestamp inicio |
| `timestamp_end` | Timestamp | Objeto Timestamp fim |

#### Criacao

```python
from pathlib import Path
from src.domain.entities.clip import ClipSegment

clip = ClipSegment(
    video_path=Path("video.mp4"),
    start=0.0,
    end=10.0,
    scene_index=1,
    silence_detected=False,
    score=0.95,
)

print(f"Duracao: {clip.duration}s")  # 10.0
```

#### Validacao

```python
from src.domain.entities.clip import ClipSegment
from src.common.exceptions import ValidationError

# Clip invalido
try:
    clip = ClipSegment(
        video_path=Path("video.mp4"),
        start=10.0,  # maior que end
        end=5.0,
    )
except ValidationError as e:
    print(f"Erro: {e}")
```

---

## 7. Configuracao

### 7.1 ProcessingConfig

Configuracao principal para processamento.

```python
class ProcessingConfig:
    """Configuracao de processamento de video"""

    visual_cut: VisualCutConfig
    """Configuracao de deteccao de cena"""

    silence: SilenceConfig
    """Configuracao de remocao de silencio"""

    subtitles: SubtitlesConfig
    """Configuracao de legendas"""

    normalize_audio: bool = False
    """Normalizar audio"""

    keep_original: bool = True
    """Manter arquivo original"""

    max_workers: int = 3
    """Workers maximos"""

    output_dir: Path | None = None
    """Diretorio de saida"""
```

### 7.2 VisualCutConfig

Configuracao para deteccao de cena.

```python
class VisualCutConfig:
    """Configuracao de deteccao de cena"""

    enabled: bool = True
    """Habilitar deteccao"""

    sensitivity: float = 1.0
    """Sensibilidade (0.1-2.0)"""

    sample_rate: int = 5
    """Taxa de amostragem (quadros/segundo)"""

    threshold: float | None = None
    """Threshold personalizado"""
```

### 7.3 SilenceConfig

Configuracao para remocao de silencio.

```python
class SilenceConfig:
    """Configuracao de remocao de silencio"""

    enabled: bool = False
    """Habilitar remocao"""

    db_threshold: int = -40
    """Threshold em dB"""

    min_duration: float = 0.5
    """Duracao minima do silencio"""
```

### 7.4 SubtitlesConfig

Configuracao para legendas.

```python
class SubtitlesConfig:
    """Configuracao de legendas"""

    enabled: bool = False
    """Habilitar geracao"""

    format: str = "srt"
    """Formato (srt/vtt)"""

    burn: bool = False
    """Inserir no video"""

    model: str = "base"
    """Modelo Whisper"""
```

### 7.5 Criacao de Configuracao

```python
from src.domain.values.config import (
    ProcessingConfig,
    VisualCutConfig,
    SilenceConfig,
    SubtitlesConfig,
)

// Configuracao simples
config = ProcessingConfig()

// Configuracao personalizada
config = ProcessingConfig(
    visual_cut=VisualCutConfig(
        enabled=True,
        sensitivity=1.2,
        sample_rate=5,
    ),
    silence=SilenceConfig(
        enabled=True,
        db_threshold=-45,
        min_duration=0.5,
    ),
    subtitles=SubtitlesConfig(
        enabled=True,
        format="srt",
    ),
    normalize_audio=True,
    max_workers=2,
)
```

---

## 8. Casos de Uso

### 8.1 SceneDetector

Detecta mudancas de cena.

```python
class SceneDetector:
    """Caso de uso para deteccao de cena"""

    def __init__(
        self,
        sensitivity: float = 1.0,
        sample_rate: int = 5,
    ) -> None:
        """Inicializa o detector.

        Args:
            sensitivity: Sensibilidade (0.1-2.0).
            sample_rate: Taxa de amostragem.
        """
        ...

    def detect(
        self,
        video_path: Path,
    ) -> list[ClipSegment]:
        """Detecta mudancas de cena.

        Args:
            video_path: Caminho do video.

        Returns:
            Lista de clips detectados.

        Raises:
            FileNotFoundError: Se o video nao existir.
        """
        ...

    def detect_with_preview(
        self,
        video_path: Path,
    ) -> Generator[ClipSegment, None, None]:
        """Detecta com preview dos quadros.

        Args:
            video_path: Caminho do video.

        Yields:
            ClipSegment para cada corte.
        """
        ...
```

#### Exemplo

```python
from pathlib import Path
from src.domain.use_cases.detect_scene import SceneDetector

detector = SceneDetector(
    sensitivity=1.0,
    sample_rate=5,
)

clips = detector.detect(Path("video.mp4"))

for clip in clips:
    print(f"Cena {clip.scene_index}: {clip.start}s - {clip.end}s")
    print(f"  Score: {clip.score}")
```

### 8.2 SilenceDetector

Detecta regions de silencio.

```python
class SilenceDetector:
    """Caso de uso para deteccao de silencio"""

    def __init__(
        self,
        db_threshold: int = -40,
        min_duration: float = 0.5,
    ) -> None:
        """Inicializa o detector.

        Args:
            db_threshold: Threshold em dB.
            min_duration: Duracao minima.
        """
        ...

    def detect(
        self,
        video_path: Path,
    ) -> list[Interval]:
        """Detecta regioes de silencio.

        Args:
            video_path: Caminho do video.

        Returns:
            Lista de intervalos de silencio.
        """
        ...

    def remove_silence(
        self,
        video_path: Path,
        output_path: Path,
    ) -> Path:
        """Remove silencio do video.

        Args:
            video_path: Caminho do video.
            output_path: Caminho de saida.

        Returns:
            Caminho do video processado.
        """
        ...
```

#### Exemplo

```python
from pathlib import Path
from src.domain.use_cases.detect_silence import SilenceDetector

detector = SilenceDetector(
    db_threshold=-40,
    min_duration=0.5,
)

silences = detector.detect(Path("video.mp4"))

for silence in silences:
    print(f"Silencio: {silence.start}s - {silence.end}s")
```

---

## 9. Adaptadores

### 9.1 FFmpegAdapter

Processamento de video com FFmpeg.

```python
class FFmpegAdapter:
    """Adaptador para FFmpeg"""

    def get_metadata(
        self,
        video_path: Path,
    ) -> VideoDocument:
        """Obtem metadados do video.

        Args:
            video_path: Caminho do video.

        Returns:
            VideoDocument com metadados.
        """
        ...

    def extract_frames(
        self,
        video_path: Path,
        output_dir: Path,
        sample_rate: int = 1,
    ) -> list[Path]:
        """Extrai quadros do video.

        Args:
            video_path: Caminho do video.
            output_dir: Diretorio de saida.
            sample_rate: Taxa de amostragem.

        Returns:
            Lista de caminhos dos quadros.
        """
        ...

    def extract_audio(
        self,
        video_path: Path,
        output_path: Path,
    ) -> Path:
        """Extrai audio do video.

        Args:
            video_path: Caminho do video.
            output_path: Caminho de saida.

        Returns:
            Caminho do audio.
        """
        ...

    def cut_video(
        self,
        video_path: Path,
        start: float,
        end: float,
        output_path: Path,
    ) -> Path:
        """Corta o video.

        Args:
            video_path: Caminho do video.
            start: Tempo de inicio.
            end: Tempo de fim.
            output_path: Caminho de saida.

        Returns:
            Caminho do video cortado.
        """
        ...

    def concatenate_videos(
        self,
        video_paths: list[Path],
        output_path: Path,
    ) -> Path:
        """Concatena videos.

        Args:
            video_paths: Lista de caminhos.
            output_path: Caminho de saida.

        Returns:
            Caminho do video concatenado.
        """
        ...

    def burn_subtitles(
        self,
        video_path: Path,
        subtitles_path: Path,
        output_path: Path,
    ) -> Path:
        """Insere legendas no video.

        Args:
            video_path: Caminho do video.
            subtitles_path: Caminho das legendas.
            output_path: Caminho de saida.

        Returns:
            Caminho do video com legendas.
        """
        ...
```

### 9.2 OpenCVAdapter

Processamento de imagem com OpenCV.

```python
class OpenCVAdapter:
    """Adaptador para OpenCV"""

    def read_frame(
        self,
        frame_path: Path,
    ) -> np.ndarray:
        """Le um quadro.

        Args:
            frame_path: Caminho do quadro.

        Returns:
            Array numpy do quadro.
        """
        ...

    def calculate_difference(
        self,
        frame1: np.ndarray,
        frame2: np.ndarray,
    ) -> float:
        """Calcula diferenca entre quadros.

        Args:
            frame1: Primeiro quadro.
            frame2: Segundo quadro.

        Returns:
            Score de diferenca.
        """
        ...

    def detect_scene_change(
        self,
        frames: list[np.ndarray],
        threshold: float = 30.0,
    ) -> list[int]:
        """Detecta mudanca de cena.

        Args:
            frames: Lista de quadros.
            threshold: Threshold de deteccao.

        Returns:
            Indices de mudanca de cena.
        """
        ...
```

### 9.3 WhisperAdapter

Transcricao de audio com Whisper.

```python
class WhisperAdapter:
    """Adaptador para Whisper"""

    def __init__(
        self,
        model: str = "base",
        device: str | None = None,
    ) -> None:
        """Inicializa o adapter.

        Args:
            model: Modelo a usar (tiny/base/small/medium/large).
            device: Dispositivo (cpu/cuda).
        """
        ...

    def transcribe(
        self,
        audio_path: Path,
    ) -> list[SubtitleEntry]:
        """Transcreve audio.

        Args:
            audio_path: Caminho do audio.

        Returns:
            Lista de legendas.
        """
        ...

    def save_subtitles(
        self,
        entries: list[SubtitleEntry],
        output_path: Path,
        format: str = "srt",
    ) -> Path:
        """Salva legendas.

        Args:
            entries: Lista de legendas.
            output_path: Caminho de saida.
            format: Formato (srt/vtt).

        Returns:
            Caminho do arquivo de legendas.
        """
        ...
```

### 9.4 AudioAdapter

Processamento de audio.

```python
class AudioAdapter:
    """Adaptador para processamento de audio"""

    def load_audio(
        self,
        audio_path: Path,
    ) -> tuple[np.ndarray, int]:
        """Carrega audio.

        Args:
            audio_path: Caminho do audio.

        Returns:
            Tuple (audio_data, sample_rate).
        """
        ...

    def get_silence_intervals(
        self,
        audio_data: np.ndarray,
        sample_rate: int,
        db_threshold: int = -40,
    ) -> list[tuple[float, float]]:
        """Obtem intervalos de silencio.

        Args:
            audio_data: Dados do audio.
            sample_rate: Taxa de amostragem.
            db_threshold: Threshold em dB.

        Returns:
            Lista de intervalos (inicio, fim).
        """
        ...

    def normalize(
        self,
        audio_data: np.ndarray,
        target_db: float = -20.0,
    ) -> np.ndarray:
        """Normaliza audio.

        Args:
            audio_data: Dados do audio.
            target_db: Volume alvo em dB.

        Returns:
            Audio normalizado.
        """
        ...

    def save_audio(
        self,
        audio_data: np.ndarray,
        sample_rate: int,
        output_path: Path,
    ) -> Path:
        """Salva audio.

        Args:
            audio_data: Dados do audio.
            sample_rate: Taxa de amostragem.
            output_path: Caminho de saida.

        Returns:
            Caminho do arquivo de audio.
        """
        ...
```

---

## 10. Exportadores

### 10.1 JSONExporter

Exporta relatrios em JSON.

```python
from src.infrastructure.exporters.json_exporter import JSONExporter

exporter = JSONExporter()

report_path = exporter.export(
    clips: list[ClipSegment],
    video_path: Path,
    output_dir: Path,
)
```

### 10.2 SRTExporter

Exporta legendas em SRT.

```python
from src.infrastructure.exporters.srt_exporter import SRTExporter

exporter = SRTExporter()

srt_path = exporter.export(
    entries: list[SubtitleEntry],
    output_path: Path,
)
```

### 10.3 VTTExporter

Exporta legendas em WebVTT.

```python
from src.infrastructure.exporters.vtt_exporter import VTTExporter

exporter = VTTExporter()

vtt_path = exporter.export(
    entries: list[SubtitleEntry],
    output_path: Path,
)
```

---

## 11. Excecoes

### 11.1 Excessoes Customizadas

| Excecao | Descricao |
|---------|------------|
| `VideoClipsError` | Erro base |
| `FileNotFoundError` | Arquivo nao encontrado |
| `ValidationError` | Erro de validacao |
| `ProcessingError` | Erro de processamento |
| `FFmpegError` | Erro do FFmpeg |
| `SubtitlesError` | Erro de legendas |

### 11.2 Tratamento de Erros

```python
from pathlib import Path
from src.application.pipeline import VideoPipeline
from src.domain.values.config import ProcessingConfig
from src.common.exceptions import VideoClipsError

try:
    pipeline = VideoPipeline()
    result = pipeline.process_single(Path("video.mp4"))
except FileNotFoundError as e:
    print(f"Video nao encontrado: {e}")
except VideoClipsError as e:
    print(f"Erro ao processar: {e}")
```

---

## 12. GUI

### 12.1 MainWindow

Interface grafica principal.

```python
from src.gui.main_window import MainWindow
from PyQt6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exec(app.exec())
```

### 12.2 Controles

| Controle | Descricao |
|----------|------------|
| `video_selector` | Selecao de video |
| `options_panel` | Painel de opcoes |
| `timeline_viewer` | Visualizador de timeline |
| `preview_player` | Reproductor de preview |
| `process_button` | Botao de processar |

---

## 13. Exemplos

### 13.1 Processamento Basico

```python
from pathlib import Path
from src.application.pipeline import VideoPipeline
from src.domain.values.config import ProcessingConfig

config = ProcessingConfig()
pipeline = VideoPipeline(config=config)

result = pipeline.process_single(Path("video.mp4"))
print(f"Clips: {result['clips_detected']}")
```

### 13.2 Processamento com Opcoes

```python
from pathlib import Path
from src.application.pipeline import VideoPipeline
from src.domain.values.config import ProcessingConfig

config = ProcessingConfig(
    visual_cut={"enabled": True, "sensitivity": 1.2},
    silence={"enabled": True, "db_threshold": -45},
    subtitles={"enabled": True, "format": "srt"},
    normalize_audio=True,
)

pipeline = VideoPipeline(config=config)

result = pipeline.process_single(Path("video.mp4"))
print(f"Status: {result['status']}")
print(f"Clips: {result['clips_detected']}")
print(f"Legendas: {result['subtitles_path']}")
```

### 13.3 Processamento em Lote

```python
from pathlib import Path
from src.application.pipeline import VideoPipeline
from src.domain.values.config import ProcessingConfig

config = ProcessingConfig()
pipeline = VideoPipeline(config=config)

videos = [
    Path("video1.mp4"),
    Path("video2.mp4"),
    Path("video3.mp4"),
]

results = pipeline.process_batch(videos)

for result in results:
    print(f"{result['video_name']}: {result['clips_detected']} clips")
```

### 13.4 Uso da CLI

```bash
# Help
python -m src.cli.commands --help

# Processar video
python -m src.cli.commands process video.mp4

# Processar com silencio
python -m src.cli.commands process video.mp4 --remove-silence

# Processar com tudo
python -m src.cli.commands process video.mp4 --visual-cut --remove-silence --normalize-audio --generate-subtitles
```

### 13.5 Uso da GUI

```bash
python -m src.cli.commands gui
```

---

## Autores

| Autor | Contato |
|------|--------|
| Dev Team | dev@video-clips.com |

---

## Licenca

MIT License - veja LICENSE para detalhes.

---

*Documentacao de API - Video Clips Automation v1.0.0*