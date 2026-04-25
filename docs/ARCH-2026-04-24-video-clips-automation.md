# Arquitetura do Sistema - Video Clips Automation

| Metadata           | Valor                                              |
| ------------------ | -------------------------------------------------- |
| **Documento**      | ARCH-2026-04-24-video-clips-automation.md          |
| **Versão**         | 1.0                                              |
| **Data**           | 2026-04-24                                       |
| **Autor**          | Tech Lead Agent                                   |
| **Status**         | Draft                                            |
| **Skill**          | software-architecture                            |
| **Parent Docs**    | REQ-2026-04-24, AC-2026-04-24, BDD-2026-04-24 |

---

## 1. Visão Geral da Arquitetura

### 1.1 Tipo de Arquitetura

| Característica | Valor |
|---------------|-------|
| **Tipo** | Modular Monolítica com CLI/GUI |
| **Padrão** | Clean Architecture (Camadas) |
| **Paradigma** | Programação Orientada a Objetos (POO) |

### 1.2 Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────────┐
│                        UI LAYER                                 │
│  ┌─────────────────┐              ┌─────────────────┐       │
│  │   CLI (Click)   │              │   GUI (PyQt6)    │       │
│  └────────┬────────┘              └────────┬────────┘       │
└───────────┼──────────────────────────────────┼────────────────┘
           │                                   │
┌──────────▼──────────────────────────────────▼────────────────┐
│                    APPLICATION LAYER                          │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              Pipeline Controller                         │ │
│  │  (Orquestra detectores, processadores e exporters)       │ │
│  └─────────────────────────────────────────────────────────┘ │
└──────────┬────────────────────────────────────┬─────────────┘
           │                                     │
┌──────────▼──────────────────┐   ┌───────────────▼──────────────────┐
│     DOMAIN LAYER          │   │        INFRASTRUCTURE LAYER        │
│  ┌───────────────────┐    │   │  ┌────────────────────────────┐   │
│  │  VideoDocument    │    │   │  │  FFmpegAdapter       │   │
│  │  (Entity)        │    │   │  │  (Video Processing) │   │
│  └───────────────────┘    │   │  └────────────────────────────┘ │
│  ┌───────────────────┐    ��   │  ┌────────────────────────────┐   │
│  │  ClipSegment     │    │   │  │  WhisperAdapter      │   │
│  │  (Entity)         │    │   │  │  (Subtitles)        │   │
│  └───────────────────┘    │   │  └────────────────────────────┘ │
│  ┌───────────────────┐    │   │  ┌────────────────────────────┐   │
│  │  SilenceDetector │    │   │  │  ReportExporter     │   │
│  │  (Use Case)      │    │   │  │  (JSON/SRT/VTT)    │   │
│  └───────────────────┘    │   │  └────────────────────────────┘ │
│  ┌───────────────────┐    │   │  ┌────────────────────────────┐   │
│  │  SceneDetector  │    │   │  │  FileSystemAdapter  │   │
│  │  (Use Case)    │    │   │  │  (I/O)             │   │
│  └───────────────────┘    │   │  └────────────────────────────┘ │
└────────────────────────────┘   └──────────────────────────────┘
```

---

## 2. Estrutura de Packages

### 2.1 Diagrama de Arquivos

```
clips_videos/
├── docs/                          # Documentação do projeto
│   ├── REQ-2026-04-24-video-clips-automation.md
│   ├── AC-2026-04-24-video-clips-automation.md
│   ├── BDD-2026-04-24-video-clips-automation.md
│   └── ARCH-2026-04-24-video-clips-automation.md
│
├── src/                          # Código fonte principal
│   ├── __init__.py
│   │
│   ├── cli/                      # Interface CLI (Click)
│   │   ├── __init__.py
│   │   ├── commands.py           # Definição de comandos
│   │   └── options.py           # Definição de opções
│   │
│   ├── gui/                      # Interface GUI (PyQt6)
│   │   ├── __init__.py
│   │   ├── main_window.py       # Janela principal
│   │   ├── preview_widget.py   # Widget de preview
│   │   ├── timeline_widget.py  # Widget de timeline
│   │   └── dialogs.py         # Diálogos
│   │
│   ├── application/             # Camada de aplicação
│   │   ├── __init__.py
│   │   ├── pipeline.py          # Orquestrador principal
│   │   ├── batch_processor.py  # Processamento em lote
│   │   └── config.py            # Gerenciador de config
│   │
│   ├── domain/                  # Camada de domínio
│   │   ├── __init__.py
│   │   ├── entities/            # Entidades
│   │   │   ├── __init__.py
│   │   │   ├── video.py         # VideoDocument
│   │   │   └── clip.py          # ClipSegment
│   │   │
│   │   ├── values/              # Value Objects
│   │   │   ├── __init__.py
│   │   │   ├── timestamp.py    # Timestamp
│   │   │   └── config.py       # Config values
│   │   │
│   │   └── use_cases/           # Casos de uso
│   │       ├── __init__.py
│   │       ├── detect_scene.py  # Detecção de cena
│   │       ├── detect_silence.py # Detecção de silêncio
│   │       └── generate_subtitles.py # Legendas
│   │
│   ├── infrastructure/          # Camada de infraestrutura
│   │   ├── __init__.py
│   │   ├── adapters/
│   │   │   ├── __init__.py
│   │   │   ├── ffmpeg_adapter.py # Processamento FFmpeg
│   │   │   ├── whisper_adapter.py # Whisper local
│   │   │   └── audio_adapter.py # Processamento áudio
│   │   │
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── video_repository.py
│   │   │   └── clip_repository.py
│   │   │
│   │   └── exporters/
│   │       ├── __init__.py
│   │       ├── json_exporter.py
│   │       ├── srt_exporter.py
│   │       └── vtt_exporter.py
│   │
│   └── common/                   # Componentes compartilhados
│       ├── __init__.py
│       ├── exceptions/          # Exceções customizadas
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── video_exceptions.py
│       │   └── processing_exceptions.py
│       │
│       ├── utils/               # Utilitários
│       │   ├── __init__.py
│       │   ├── logger.py        # Logging
│       │   └── validators.py    # Validadores
│       │
│       └── logging/
│           ├── __init__.py
│           └── setup.py         # Setup de logging
│
├── tests/                         # Testes unitários
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── domain/
│   │   │   ├── __init__.py
│   │   │   ├── test_entities.py
│   │   │   └── test_use_cases.py
│   │   └── infrastructure/
│   │       ├── __init__.py
│   │       └── test_adapters.py
│   │
│   └── integration/
│       ├── __init__.py
│       └── test_pipeline.py
│
├── configs/                      # Arquivos de configuração
│   ├── config.example.json
│   └── logging.example.yaml
│
├── requirements.txt              # Dependências Python
├── setup.py                     # Script de setup
├── README.md                   # Documentação principal
├── Makefile                    # Comandos úteis
└── .gitignore                  # Git ignore
```

---

## 3. Decisões Arquiteturais

### 3.1 Technology Stack

| Componente | Tecnologia | Justificativa |
|------------|------------|--------------|
| **CLI** | Click | Simples, já utilizado no projeto |
| **GUI** | PyQt6 | Requisito do usuário |
| **Vídeo** | OpenCV, FFmpeg | Análise de frames e corte |
| **Áudio** | pydub, scipy | Detecção de silêncio |
| **Legendas** | Whisper (local) | Requisito do usuário |
| **Paralelização** | multiprocessing + threading | CPU-bound + I/O |
| **Logging** | Python logging | Padrão Python |
| **Config** | JSON | Requisito do usuário |

### 3.2 Padrões de Projeto

| Padrão | Aplicação | Local |
|--------|-----------|-------|
| **Factory** | Criação de adaptadores | `infrastructure/adapters/` |
| **Strategy** | Detecção de cena/silêncio | `domain/use_cases/` |
| **Observer** | Progresso de processamento | `gui/timeline_widget.py` |
| **Template Method** | Pipeline de processamento | `application/pipeline.py` |
| **Repository** | Acesso a arquivos | `infrastructure/repositories/` |

### 3.3 Dependency Injection

```python
# Exemplo de DI via functools
from functools import lru_cache

@lru_cache()
def get_ffmpeg_adapter() -> FFmpegAdapter:
    return FFmpegAdapter()

@lru_cache()
def get_whisper_adapter() -> WhisperAdapter:
    return WhisperAdapter()
```

---

## 4. Fluxo de Processamento

### 4.1 Pipeline Principal

```
┌──────────────��     ┌──────────────┐     ┌──────────────┐
│  Load Video  │ ──▶ │  Analyze    │ ──▶ │  Detect     │
│  (VideoDoc)  │     │  Frames     │     │  Cuts       │
└──────────────┘     └──────────────┘     └──────────────┘
                                                 │
                     ┌───────────────────────────┼───────────────────────────┐
                     │                           │                           │
              ┌──────▼──────┐          ┌───────▼───────┐          ┌──────▼──────┐
              │ Scene       │          │ Silence       │          │ Manual      │
              │ Detection   │          │ Detection    │          │ Timestamps │
              └──────┬──────┘          └───────┬───────┘          └──────┬──────┘
                     │                           │                           │
                     └───────────────────────────┼───────────────────────────┘
                                                 │
                                      ┌──────────▼──────────┐
                                      │  Merge Results     │
                                      │  (ClipSegments)   │
                                      └─────────┬────────────┘
                                                │
                           ┌──────────────────────┼──────────────────────┐
                           │                      │                      │
                    ┌──────▼──────┐       ┌──────▼──────┐       ┌──────▼──────┐
                    │  Cut Video  │       │  Remove     │       │  Generate   │
                    │  (FFmpeg)  │       │  Silence    │       │  Subtitles  │
                    └──────┬──────┘       └──────┬──────┘       └──────┬──────┘
                           │                      │                      │
                           └──────────────────────┼──────────────────────┘
                                                    │
                                         ┌────────▼────────┐
                                         │  Export Output │
                                         │  (JSON/SRT)    │
                                         └────────────────┘
```

### 4.2 Batch Processing

```
┌──────────────┐
│  Load Files │
│  from Batch │
└──────┬──────┘
       │
┌──────▼──────────────────────────────────────────┐
│           Worker Pool (3 workers)               │
│  ┌────────┐  ┌────────┐  ┌────────┐           │
│  │Worker 1│  │Worker 2│  │Worker 3│           │
│  │ ─►     │  │ ─►     │  │ ─►     │           │
│  │MP4     │  │MP4     │  │MP4     │           │
│  └────────┘  └────────┘  └────────┘           │
└──────┬──────────────────────────────────────────┘
       │
┌──────▼──────────┐
│  Merge Reports │
└───────────────┘
```

---

## 5. Interfaces (Ports)

### 5.1 VideoProcessor Port

```python
from abc import ABC, abstractmethod
from typing import List
from domain.entities.clip import ClipSegment

class VideoProcessorPort(ABC):
    """Port para processador de vídeo"""

    @abstractmethod
    def cut_video(self, input_path: str, clips: List[ClipSegment], output_dir: str) -> List[str]:
        """Corta vídeo em clips"""
        pass

    @abstractmethod
    def remove_silence(self, input_path: str, silence_ranges: List[tuple], output_path: str) -> str:
        """Remove silêncio do vídeo"""
        pass
```

### 5.2 SceneDetector Port

```python
class SceneDetectorPort(ABC):
    """Port para detector de cena"""

    @abstractmethod
    def detect(self, video_path: str, sensitivity: float) -> List[ClipSegment]:
        """Detecta mudanças de cena"""
        pass
```

### 5.3 SubtitleGenerator Port

```python
class SubtitleGeneratorPort(ABC):
    """Port para gerador de legendas"""

    @abstractmethod
    def generate(self, audio_path: str, format: str) -> str:
        """Gera legendas em formato SRT/VTT"""
        pass

    @abstractmethod
    def burn_subtitles(self, video_path: str, subtitle_path: str, output_path: str) -> str:
        """Insere legendas no vídeo"""
        pass
```

---

## 6. Configurações

### 6.1 Configuração Padrão (JSON)

```json
{
  "processing": {
    "visual_cut": {
      "enabled": true,
      "sensitivity": 1.0,
      "sample_rate": 5
    },
    "silence_removal": {
      "enabled": false,
      "db_threshold": -40,
      "min_duration": 0.5
    },
    "normalization": {
      "enabled": false
    }
  },
  "subtitles": {
    "enabled": false,
    "format": "srt",
    "burn": false,
    "whisper_model": "base"
  },
  "output": {
    "format": "same",
    "quality": "original",
    "keep_original": true,
    "max_workers": 3
  },
  "logging": {
    "level": "INFO",
    "file": "app.log"
  }
}
```

### 6.2 CLI Options Mapping

| Flag | Config Path | Tipo |
|------|------------|------|
| `--visual-cut` | `processing.visual_cut.enabled` | bool |
| `--sensitivity` | `processing.visual_cut.sensitivity` | float |
| `--remove-silence` | `processing.silence_removal.enabled` | bool |
| `--silence-db` | `processing.silence_removal.db_threshold` | int |
| `--silence-duration` | `processing.silence_removal.min_duration` | float |
| `--normalize-audio` | `processing.normalization.enabled` | bool |
| `--generate-subtitles` | `subtitles.enabled` | bool |
| `--export-subtitles` | `subtitles.format` | str |
| `--burn-subtitles` | `subtitles.burn` | bool |
| `--destroy` | `output.keep_original` | bool |
| `--no-audio` | `processing.no_audio` | bool |
| `--batch` | input | path |
| `--config` | config file | path |

---

## 7. Handling de Erros

### 7.1 Exceções Customizadas

| Exceção | Herda de | Quando ocorre |
|---------|---------|---------------|
| `VideoNotFoundError` | `VideoException` | Arquivo não encontrado |
| `VideoCorruptedError` | `VideoException` | Vídeo ilegível |
| `FFmpegNotFoundError` | `ProcessingException` | FFmpeg não instalado |
| `WhisperError` | `ProcessingException` | Falha na transcrição |
| `ProcessingError` | `BaseException` | Erro genérico |

### 7.2 Strategy de Error Handling

```python
# Por padrão: continuar com warning
# Com --strict: abortar tudo

def process_batch(videos: List[str], strict: bool = False):
    results = []
    for video in videos:
        try:
            result = process_single(video)
            results.append(result)
        except ProcessingError as e:
            if strict:
                raise
            logger.warning(f"Erro em {video}: {e}")
            results.append({"error": str(e)})
    return results
```

---

## 8. Testes

### 8.1 Estratégia de Testes

| Tipo | Cobertura | Framework |
|------|-----------|-----------|
| **Unit** | Entidades, Use Cases, Adapters | pytest |
| **Integration** | Pipeline completo | pytest |
| **E2E** | CLI e GUI | PyTest + subprocess |

### 8.2 Testes Principais

| Módulo | Testes |
|--------|-------|
| `domain/entities` | VideoDocument, ClipSegment |
| `domain/use_cases` | SceneDetector, SilenceDetector |
| `infrastructure/adapters` | FFmpegAdapter, WhisperAdapter |
| `application` | Pipeline, BatchProcessor |

---

## 9. Próximos Passos

| #   | Ação                                 | Responsável |
| --- | ------------------------------------ | -------------|
| 1   | Criar estrutura de packages         | Tech Lead    |
| 2   | Implementar entidades do domínio    | Developer   |
| 3   | Implementar adaptadores              | Developer   |
| 4   | Implementar casos de uso            | Developer   |
| 5   | Implementar CLI                    | Developer   |
| 6   | Implementar GUI                   | Developer   |
| 7   | Implementar testes                | Test Agent  |

---

## 10. Dependências Externas Requeridas

| Dependência | Versão Mínima | Uso |
|------------|--------------|-----|
| `click` | 8.2.1 | CLI |
| `PyQt6` | 6.x | GUI |
| `opencv-python` | 4.13.0 | Análise de frames |
| `ffmpeg-python` | 0.2.0 | Wrapper FFmpeg |
| `pydub` | 0.25.1 | Processamento áudio |
| `whisper` | latest | Legendas locais |
| `torch` | 2.x | Whisper |
| `numpy` | 1.x | Processamento numérico |
| `pytest` | 7.x | Testes |

---

*Documento gerado pelo Tech Lead Agent - Skills: software-architecture*