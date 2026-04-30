# Arquivo de Configuração

O arquivo de configuração permite salvar todas as opções de processamento em um arquivo JSON, para reuse em futuros processamentos.

## Visão Geral

Ao invés de digitar todas as opções na linha de comando, você pode:

- Criar um arquivo de configuração JSON
- Usar o mesmo arquivo para múltiplos vídeos
- Compartilhar configurações com outros

---

## Criando um Arquivo de Configuração

### Método 1: Comando init-config

A forma mais simples de criar um arquivo de configuração:

```bash
python -m src.cli.commands init-config
```

Isso cria um arquivo `config.example.json` com todas as opções padrão.

### Método 2: Criar Manualmente

Você pode criar o arquivo manualmente usando qualquer editor de texto:

```json
{
  "processing": {
    "visual_cut": {
      "enabled": true,
      "sensitivity": 1.0,
      "sample_rate": 5,
      "min_clip_duration": 0.0
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

### Método 3: Via Python

```python
from src.domain.values.config import ProcessingConfig

config = ProcessingConfig()
config.visual_cut.enabled = True
config.visual_cut.sensitivity = 1.5
config.silence.enabled = True

config.save_json(Path("minha_config.json"))
```

---

## Estrutura do Arquivo JSON

### Seção: processing

Configurações do processamento de vídeo.

#### visual_cut

| Campo | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `enabled` | booleano | true | Ativar detecção de cena |
| `sensitivity` | número | 1.0 | Sensibilidade (0.3=baixa, 1.0=média, 2.0=alta) |
| `sample_rate` | número | 5 | Analisar a cada N frames |
| `min_clip_duration` | número | 0.0 | Duração mínima do clip em segundos (0=sem limite, >0 = clips com mais de X segundos) |

**Exemplo:**

```json
"visual_cut": {
  "enabled": true,
  "sensitivity": 1.5,
  "sample_rate": 3,
  "min_clip_duration": 4.0
}
```

#### silence_removal

| Campo | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `enabled` | booleano | false | Ativar remoção de silêncio |
| `db_threshold` | número | -40 | Threshold em dB |
| `min_duration` | número | 0.5 | Duração mínima em segundos |

**Exemplo:**

```json
"silence_removal": {
  "enabled": true,
  "db_threshold": -45,
  "min_duration": 1.0
}
```

#### normalization

| Campo | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `enabled` | booleano | false | Ativar normalização |

**Exemplo:**

```json
"normalization": {
  "enabled": true
}
```

---

### Seção: subtitles

Configurações de legendas.

| Campo | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `enabled` | booleano | false | Ativar geração de legendas |
| `format` | texto | "srt" | Formato: srt ou vtt |
| `burn` | booleano | false | Queimar legendas no vídeo |
| `whisper_model` | texto | "base" | Modelo Whisper: tiny, base, small, medium |

**Exemplo:**

```json
"subtitles": {
  "enabled": true,
  "format": "vtt",
  "burn": true,
  "whisper_model": "small"
}
```

---

### Seção: output

Configurações de saída.

| Campo | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `format` | texto | "same" | Formato de saída: same, mp4, mkv |
| `quality` | texto | "original" | Qualidade: original, high, medium, low |
| `keep_original` | booleano | true | Manter arquivo original |
| `max_workers` | número | 3 | Workers parallel |

**Exemplo:**

```json
"output": {
  "format": "mp4",
  "quality": "high",
  "keep_original": true,
  "max_workers": 4
}
```

---

### Seção: logging

Configurações de log.

| Campo | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `level` | texto | "INFO" | Nível: DEBUG, INFO, WARNING, ERROR |
| `file` | texto | "app.log" | Arquivo de log |

**Exemplo:**

```json
"logging": {
  "level": "DEBUG",
  "file": "processamento.log"
}
```

---

## Usando o Arquivo de Configuração

### CLI

```bash
python -m src.cli.commands process video.mp4 -c minha_config.json
```

### Python

```python
from src.domain.values.config import ProcessingConfig
from pathlib import Path

config = ProcessingConfig.from_json(Path("minha_config.json"))
pipeline = VideoPipeline(config=config)
result = pipeline.process_single(Path("video.mp4"))
```

---

## Exemplos de Configuração

### Exemplo 1: Clips para Redes Sociais

Vídeos curtos para TikTok ou Reels:

```json
{
  "processing": {
    "visual_cut": {
      "enabled": true,
      "sensitivity": 2.0,
      "sample_rate": 3
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
    "burn": true,
    "whisper_model": "base"
  },
  "output": {
    "format": "mp4",
    "quality": "high",
    "keep_original": true,
    "max_workers": 3
  }
}
```

### Exemplo 2: Videos para YouTube

Para vídeos mais longos com legendas:

```json
{
  "processing": {
    "visual_cut": {
      "enabled": true,
      "sensitivity": 1.0,
      "sample_rate": 5
    },
    "normalization": {
      "enabled": true
    }
  },
  "subtitles": {
    "enabled": true,
    "format": "srt",
    "burn": false,
    "whisper_model": "small"
  },
  "output": {
    "format": "same",
    "quality": "original",
    "keep_original": true,
    "max_workers": 4
  }
}
```

### Exemplo 3: Processamento Rápido

Para processar muitos vídeos rapidamente:

```json
{
  "processing": {
    "visual_cut": {
      "enabled": true,
      "sensitivity": 1.0,
      "sample_rate": 10
    }
  },
  "output": {
    "keep_original": true,
    "max_workers": 6
  }
}
```

---

## Precedência de Opções

Quando você usa um arquivo de configuração combinação com opções da CLI, a ordem de precedência é:

1. **Opções da CLI** (maior prioridade)
2. **Arquivo de configuração**
3. **Valores padrão** (menor prioridade)

**Exemplo:**

```bash
# A opção --sensitivity da CLI sobrescreve o valor do config.json
python -m src.cli.commands process video.mp4 -c config.json --sensitivity high
```

---

## Dicas

### Compartilhar Configurações

Você pode compartilhar o arquivo de configuração com sua equipe:

```bash
# Enviar o arquivo
scp minha_config.json equipe@servidor:/caminho/
```

### Versionar Configurações

Recomendamos versionar seus arquivos de configuraç��o:

```
configs/
├── v1_default.json
├── v2_youtube.json
├── v3_tiktok.json
└── v4_batch.json
```

### Validação

Para validar um arquivo de configuração:

```python
import json
from pathlib import Path

try:
    with open("config.json") as f:
        config = json.load(f)
    print("Configuração válida!")
except json.JSONDecodeError as e:
    print(f"Erro: {e}")
```

---

## Próximos Passos

- **[Detecção de Cenas](../features/scene-detection.md)** - Entenda como funciona
- **[Legendas](../features/subtitles.md)** - Detalhes sobre legendas
- **[Exemplos](../examples/index.md)** - Mais exemplos

---

## Suporte

Para problemas com configuração, veja **[Solução de Problemas](../troubleshooting.md)**.

---

*Última atualização: 2026-04-29*