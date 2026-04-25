# Guia do Desenvolvedor - Video Clips Automation

| Metadata | Valor |
|----------|-------|
| **Versão** | 1.0.0 |
| **Data** | 2026-04-24 |
| **Maintainer** | Dev Team |

---

## Table of Contents

1. [Introdução](#1-introdução)
2. [Configuração do Ambiente](#2-configuração-do-ambiente)
3. [Arquitetura do Projeto](#3-arquitetura-do-projeto)
4. [Código de Conduta](#4-código-de-conduta)
5. [Processo de Desenvolvimento](#5-processo-de-desenvolvimento)
6. [Padrões de Código](#6-padrões-de-código)
7. [Testes](#7-testes)
8. [Commits e Mensagens](#8-commits-e-mensagens)
9. [Pull Requests](#9-pull-requests)
10. [Release](#10-release)

---

## 1. Introdução

### 1.1 Visão Geral

Este guia é para desenvolvedores que desejam contribuir para o projeto Video Clips Automation. Por favor, leia este documento antes de começar a contribuir.

### 1.2 Recursos

| Recurso | Link |
|--------|------|
| Código Fonte | GitHub Repository |
| Issues | GitHub Issues |
| Discussions | GitHub Discussions |
| License | LICENSE |

---

## 2. Configuração do Ambiente

### 2.1 Pré-requisitos

- Python 3.10+
- Git
- FFmpeg

### 2.2 Configuração

1. **clone o repositório:**

```bash
git clone https://github.com/user/clips_videos.git
cd clips_videos
```

2. **Crie um ambiente virtual:**

```bash
python -m venv .venv
.\.venv\Scripts\activate.bat  # Windows
# source .venv/bin/activate  # Linux/Mac
```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy pre-commit
```

4. **Configure o pre-commit:**

```bash
pre-commit install
```

### 2.3 Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `VIDEO_CLIPS_FFMPEG_PATH` | Caminho do FFmpeg | imageio_ffmpeg |
| `VIDEO_CLIPS_LOG_LEVEL` | Nível de log | INFO |
| `VIDEO_CLIPS_MAX_WORKERS` | Workers máximo | 3 |

---

## 3. Arquitetura do Projeto

### 3.1 Visão Geral da Arquitetura

```
src/
├── cli/                    # Command Line Interface
│   └── commands.py        # Comandos Click
├── gui/                    # Graphical User Interface
│   └── main_window.py      # Interface PyQt6
├── application/            # Orquestrador principal
│   └── pipeline.py        # Pipeline de processamento
├── domain/                 # Entidades e casos de uso
│   ├── entities/          # Entidades do domínio
│   │   ├── clip.py        # ClipSegment
│   │   └── video.py       # VideoDocument
│   ├── values/            # Value Objects
│   │   ├── config.py      # ProcessingConfig
│   │   └── timestamp.py   # Timestamp
│   └── use_cases/         # Casos de uso
│       ├── detect_scene.py
│       └── detect_silence.py
├── infrastructure/         # Adaptadores externos
│   ├── adapters/          # Adaptadores
│   │   ├── ffmpeg_adapter.py
│   │   ├── opencv_adapter.py
│   │   ├── whisper_adapter.py
│   │   └── audio_adapter.py
│   └── exporters/         # Exportadores
│       ├── json_exporter.py
│       ├── srt_exporter.py
│       └── vtt_exporter.py
└── common/                # Código comum
    ├── exceptions.py      # Exceções customizadas
    └── utils.py           # Utilitários
```

### 3.2 Fluxo de Processamento

```
Input Video
    │
    ▼
┌─────────────────┐
│ VideoPipeline  │ ◄── Orquestra todo o processo
└─────────────────┘
    │
    ├──▶ VideoMetadata ───▶ OpenCVAdapter ──▶ Detectar cena
    │                                         │
    ├──▶ AudioTrack ──────▶ AudioAdapter ──▶ Remover silêncio
    │                                         │
    └──▶ Subtitles ──────▶ WhisperAdapter ──▶ Gerar legendas
                                                   │
                                                     ▼
                                              Output Clips/
```

### 3.3 Padrão de Arquitetura

O projeto segue o padrão de arquitetura **Hexagonal** (Ports and Adapters):

| Camada | Responsabilidade |
|--------|-----------------|
| **Domain** | Entidades, Value Objects, Casos de Uso |
| **Application** | Pipeline, Casos de Uso |
| **Infrastructure** | Adaptadores externos (FFmpeg, OpenCV, Whisper) |
| **CLI/GUI** | Interfaces de usuário |

---

## 4. Código de Conduta

### 4.1 Nosso Compromisso

Para promover um ambiente aberto e acolhedor, nós comprometemos a tornar a participação em nosso projeto uma experiência livre de assédio para todos.

### 4.2 Standards

Exemplos de comportamento que contribuem para um ambiente positivo:

- Usar linguagem acolhedora e inclusiva
- Ser respeitoso com diferentes pontos de vista e experiências
- Aceitar críticas construtivas com graciosidade
- Focar no que é melhor para a comunidade
- Mostrar empatia para com outros membros da comunidade

### 4.3 Nossas Responsabilidades

Os mantenedores são responsáveis por clarificar os padrões de comportamento aceitável e devem tomar ações corretivas apropriadas em resposta a_instances de comportamento inaceitável.

---

## 5. Processo de Desenvolvimento

### 5.1 Branch Strategy

```
main ◄──────────── Merge de feature branches
 │
 ├── feature/nova-funcionalidade
 │   └── Base: main
 │   
 ├── bugfix/fix-algum-bug
 │   └── Base: main
 │
 └── hotfix/urgente
     └── Base: main
```

### 5.2 Workflow

| Passo | Ação | Descrição |
|-------|------|-----------|
| 1 | Escolher issue | Escolha um issue do backlog |
| 2 | Criar branch | Crie uma branch a partir da main |
| 3 | Desenvolver | Implemente a feature/fix |
| 4 | Testar | Rode os testes localmente |
| 5 | Commitar | Faça commits atômicos |
| 6 | Push | Faça push para o remoto |
| 7 | Revisar | Solicite code review |
| 8 | Merge | Faz merge após aprovação |

### 5.3 Issue Labels

| Label | Descrição |
|-------|-----------|
| `bug` | Bug报告 |
| `enhancement` | Nova funcionalidade |
| `good first issue` | Boa primeira contribuição |
| `help wanted` | Ajuda necessária |
| `documentation` | Documentação |

---

## 6. Padrões de Código

### 6.1 Padrões de Python

O projeto segue **PEP 8** com as seguintes exceções:

- **Máximo de linha:** 120 caracteres
- **Aspas:** Aspas duplas para strings, aspas simples para caracteres

```python
# Bom
def process_video(
    video_path: Path,
    config: ProcessingConfig,
) -> dict:
    """Processa um vídeo com a configuração"""
    logging.info("Processando vídeo: %s", video_path)
    return {"status": "success"}
```

```python
# Ruim
def process_video(video_path, config):
    logging.info('Processando vídeo: %s' % video_path)
    return {'status': 'success'}
```

### 6.2 Padrões de Type Hints

```python
# Sempre use type hints
def process_single(
    self,
    video: VideoDocument,
    config: ProcessingConfig,
) -> dict[str, Any]:
    ...
```

### 6.3命名ação

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Funções | snake_case | `detect_scene()`, `remove_silence()` |
| Classes | PascalCase | `VideoPipeline`, `ClipSegment` |
| Constantes | UPPER_SNAKE | `MAX_WORKERS = 3` |
| Arquivos | snake_case | `video_pipeline.py` |

### 6.4 Imports

Use `isort` para organizar imports:

```python
# Primeiro: libs padrão
import logging
from pathlib import Path
from typing import Any

# Segundo: libs de terceiros
import click
import cv2
from pydantic import Field

# Terceiro: módulos locais
from src.application.pipeline import VideoPipeline
from src.domain.entities.clip import ClipSegment
from src.domain.values.config import ProcessingConfig
```

### 6.5 Docstrings

Use o formato **Google**:

```python
def detect_scenes(
    video_path: Path,
    sensitivity: float = 1.0,
    sample_rate: int = 5,
) -> list[ClipSegment]:
    """Detecta mudanças de cena em um vídeo.

    Args:
        video_path: Caminho para o arquivo de vídeo.
        sensitivity: Sensibilidade da detecção (0.1-2.0).
        sample_rate: Taxa de amostragem (quadros por segundo).

    Returns:
        Lista de ClipSegment detectados.

    Raises:
        FileNotFoundError: Se o vídeo não for encontrado.
        ValueError: Se o vídeo não puder ser processado.
    """
    ...
```

---

## 7. Testes

### 7.1 Estrutura de Testes

```
tests/
├── unit/
│   ├── test_clip.py
│   ├── test_config.py
│   ├── test_detect_scene.py
│   └── test_detect_silence.py
├── integration/
│   └── test_pipeline.py
└── conftest.py
```

### 7.2 Rodando Testes

```bash
# Todos os testes
pytest

# Testes unitários
pytest tests/unit/

# Testes de integração
pytest tests/integration/

# Com coverage
pytest --cov=src tests/

# Teste específico
pytest tests/unit/test_clip.py -v
```

### 7.3 Padrões de Testes

```python
import pytest
from pathlib import Path
from src.domain.entities.clip import ClipSegment


class TestClipSegment:
    """Testes para ClipSegment"""

    def test_create_clip(self, tmp_path):
        """Testa criação de clip"""
        video = tmp_path / "video.mp4"
        video.write_text("dummy")

        clip = ClipSegment(
            video_path=video,
            start=0.0,
            end=10.0,
        )

        assert clip.duration == 10.0
        assert clip.start < clip.end

    def test_invalid_timestamp(self):
        """Testa timestamp inválido"""
        with pytest.raises(ValueError):
            ClipSegment(
                video_path=Path("video.mp4"),
                start=10.0,  # maior que end
                end=5.0,
            )
```

### 7.4 Mocking

Use `pytest-mock` para mocking:

```python
def test_process_with_mock(mocker):
    """Testa processamento com mock"""
    mock_ffmpeg = mocker.patch("src.infrastructure.adapters.ffmpeg_adapter.get_ffmpeg_path")
    mock_ffmpeg.return_value = "/usr/bin/ffmpeg"

    # Teste aqui
    ...
```

---

## 8. Commits e Mensagens

### 8.1 Mensagens de Commit

Use o padrão **Conventional Commits**:

```
<tipo>(<escopo>): <descrição>

[corpo opcional]

[notas de footer opcionais]
```

| Tipo | Descrição |
|------|-----------|
| `feat` | Nova funcionalidade |
| `fix` | Bug fix |
| `docs` | Documentação |
| `style` | Formatação |
| `refactor` | Refatoração |
| `test` | Testes |
| `chore` | Tarefas |

### 8.2 Exemplos

```bash
# Bom
git commit -m "feat(detect_scene): adiciona detecção de mudança de cena"

git commit -m "fix(silence): ajusta threshold de silêncio

O threshold padrão de -40dB estava muito baixo para vídeos
com música de fundo.

Closes #123"

# Ruim
git commit -m "update"
git commit -m "fix stuff"
```

### 8.3 Boas Práticas

- Commits atômicos (uma mudança por commit)
- Comece com verbo no imperativo
- Use o corpo para explicar o "porquê"
- Referencie issues quando aplicável

---

## 9. Pull Requests

### 9.1 Checklist

Antes de abrir um PR, certifique-se:

- [ ] Tests estão passando
- [ ] Code stylePassed (black, flake8)
- [ ] Type checking passou (mypy)
- [ ] Coverage não decreased
- [ ] Documentação atualizada
- [ ] Commits organizados

### 9.2 Template de PR

```markdown
## Descrição
Breve descrição da mudança.

## Tipo de Mudança
- [ ] Nova funcionalidade
- [ ] Bug fix
- [ ] Breaking change
- [ ] Documentação

## Como Testar
Passos para testar a mudança.

## Screenshots
Se aplicável.

## Checklist
- [ ] Testes adicionados/atualizados
- [ ] Docs atualizadas
- [ ] Type hints atualizados
```

### 9.3 Processo de Review

| Passo | Responsável | Ação |
|-------|-------------|------|
| 1 | Author | Abre PR |
| 2 | Reviewer | Revisa código |
| 3 | Author | Corrige issues |
| 4 | Reviewer | Aprova PR |
| 5 | Mantenedor | Faz merge |

---

## 10. Release

### 10.1 Versioning

O projeto segue **Semantic Versioning**:

```
MAJOR.MINOR.PATCH
  │    │    └── Bug fixes
  │    └──── Nova funcionalidade (backwards compatible)
  └─────── Breaking changes
```

### 10.2 Processo de Release

| Passo | Ação | Descrição |
|-------|------|-----------|
| 1 | Atualizar CHANGELOG | Documentar mudanças |
| 2 | Atualizar versão | Bump version em setup.py |
| 3 | Tag | Criar tag git |
| 4 | Build | Criar distribuição |
| 5 | Publish | Publicar no PyPI |

### 10.3 Changelog

```markdown
## [1.0.0] - 2026-04-24

### Added
- Detecçãoautomática de cena
- Remoçãoautomática de silêncio
- Geração de legendas com Whisper

### Fixed
- CLI flag --visual-cut não estava funcionando
- FFmpeg não encontrado em ambiente Windows
```

---

## Contato

| Canal | Link |
|-------|------|
| GitHub | github.com/user/clips_videos |
| Issues | github.com/user/clips_videos/issues |
| Discussions | github.com/user/clips_videos/discussions |

---

*Guia do Desenvolvedor - Video Clips Automation v1.0.0*