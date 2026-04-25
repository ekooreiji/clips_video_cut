# Video Clips Automation

| Badge | Info |
|-------|------|
| Versão | 1.0.0 |
| Licença | MIT |
| Python | 3.10+ |
| Status | Beta |

---

Sistema CLI/GUI para automatizar cortes de vídeos baseado em detecção de mudança de cena e remoção de silêncio em áudio, com suporte a legendas automáticas via Whisper local.

## 🚀 Funcionalidades

| Funcionalidade | Descrição |
|----------------|-----------|
| **Corte Automático** | Detecta mudanças de cena automaticamente via análise visual |
| **Remoção de Silêncio** | Remove trechos silenciosos do áudio |
| **Normalização** | Normaliza volume do áudio |
| **Legendas** | Gera legendas automáticas com Whisper |
| **Interface CLI** | Linha de comando completa com opções |
| **Interface GUI** | Interface gráfica com PyQt6 |
| **Processamento em Lote** | Processa múltiplos vídeos |
| **Portátil** | Executável em USB |

---

## 📦 Instalação

### Pré-requisitos

- Python 3.10+
- FFmpeg (para processamento de vídeo)

### Instalação via pip

```bash
# Clonar ou baixar
git clone https://github.com/user/clips_videos.git
cd clips_videos

# Criar ambiente virtual
python -m venv .venv
.\.venv\Scripts\activate.bat  # Windows
# source .venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Instalar FFmpeg (Windows - via Chocolatey)
choco install ffmpeg

# Ou manual: https://ffmpeg.org/download.html
```

---

## 🎮 Uso

### CLI - Linha de Comando

```bash
# Ver help
python -m src.cli.commands --help

# Processar vídeo com detecção de cena
python -m src.cli.commands process video.mp4 --visual-cut

# Processar vídeo com remoção de silêncio
python -m src.cli.commands process video.mp4 --remove-silence

# Processar com todas as opções
python -m src.cli.commands process video.mp4 --visual-cut --remove-silence --normalize-audio --generate-subtitles

# Processar todos os vídeos de uma pasta
python -m src.cli.commands process video.mp4 --batch ./videos

# Criar arquivo de configuração
python -m src.cli.commands init-config -o config.json
```

### Opções da CLI

| Flag | Descrição | Padrão |
|------|-----------|--------|
| `--visual-cut` | Detectar mudanças de cena | Ativo |
| `--sensitivity` | Sensibilidade (low/medium/high) | medium |
| `--remove-silence` | Remover silêncio | Inativo |
| `--silence-db` | Threshold dB | -40 |
| `--silence-duration` | Duração mínima (s) | 0.5 |
| `--normalize-audio` | Normalizar volume | Inativo |
| `--generate-subtitles` | Gerar legendas | Inativo |
| `--export-subtitles` | Formato (srt/vtt) | srt |
| `--burn-subtitles` | Inserir legendas no vídeo | Inativo |
| `--destroy` | Excluir original | Inativo |
| `--config` | Arquivo JSON | - |
| `--batch` | Pasta com vídeos | - |
| `-v, --verbose` | Log verboso | - |

### GUI - Interface Gráfica

```bash
# Abrir interface GUI
python -m src.cli.commands gui
```

### API Python

```python
from pathlib import Path
from src.application.pipeline import VideoPipeline
from src.domain.values.config import ProcessingConfig

# Configuração
config = ProcessingConfig()
config.visual_cut.enabled = True
config.visual_cut.sensitivity = 1.0
config.silence.enabled = True
config.silence.db_threshold = -40

# Pipeline
pipeline = VideoPipeline(config=config)
result = pipeline.process_single(Path("video.mp4"))

print(f"Clips: {result['clips_detected']}")
print(f"Relatório: {result['report_path']}")
```

---

## 📁 Estrutura do Projeto

```
clips_videos/
├── src/
│   ├── cli/              # Interface CLI
│   ├── gui/              # Interface GUI (PyQt6)
│   ├── application/       # Pipeline principal
│   ├── domain/          # Entidades e Casos de Uso
│   │   ├── entities/   # VideoDocument, ClipSegment
│   │   ├── values/     # Timestamp, ProcessingConfig
│   │   └── use_cases/  # SceneDetector, SilenceDetector
│   ├── infrastructure/    # Adaptadores
│   │   ├── adapters/  # FFmpeg, OpenCV, Whisper
│   │   └── exporters/ # JSON, SRT, VTT
│   └── common/           # Utils e Exceções
├── tests/               # Testes
│   ├── unit/          # Testes unitários
│   └── integration/   # Testes de integração
├── configs/            # Configurações
├── docs/              # Documentação
├── requirements.txt   # Dependências
├── setup.py           # Setup
└── README.md         # Este arquivo
```

---

## 📋 Configuração

### Arquivo JSON

```json
{
  "processing": {
    "visual_cut": {
      "enabled": true,
      "sensitivity": 1.0,
      "sample_rate": 5
    },
    "silence_removal": {
      "enabled": true,
      "db_threshold": -40,
      "min_duration": 0.5
    }
  },
  "subtitles": {
    "enabled": true,
    "format": "srt",
    "burn": false
  },
  "output": {
    "keep_original": true,
    "max_workers": 3
  }
}
```

---

## 🧪 Testes

```bash
# Todos os testes
pytest

# Testes unitários
pytest tests/unit/

# Testes de integração
pytest tests/integration/

# Com coverage
pytest --cov=src tests/
```

---

## 🔧 Desenvolvimento

```bash
# Setup de desenvolvimento
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy pre-commit

# Verificar código
black --check src/
flake8 src/

# Type checking
mypy src/
```

---

## ⚠️ Problemas Conhecidos

| Problema | Solução |
|----------|----------|
| FFmpeg não encontrado | Instale o FFmpeg e adicione ao PATH |
| Whisper lento no primeiro uso | Modelo será baixado na primeira execução |
| Memória alta com vídeos grandes | Reduza max_workers no config |

---

## 📝 Licença

MIT License - see LICENSE file for details.

---

## 🤝 Contribuição

1. Fork o projeto
2. Crie sua branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'feat: nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

Feito com ❤️ por Video Clips Team