# Processamento em Lote

O processamento em lote permite processar múltiplos vídeos de uma vez, economizando tempo.

## Como Funciona

Você especifica uma pasta contendo vídeos, e o sistema processa todos automaticamente:

```
pasta_videos/
├── video1.mp4    → clip_001.mp4, clip_002.mp4...
├── video2.mp4    → clip_001.mp4, clip_002.mp4...
├── video3.avi    → clip_001.mp4, clip_002.mp4...
└── video4.mkv    → clip_001.mp4, clip_002.mp4...
```

---

## Formatos Suportados

| Extensão | Tipo |
|----------|------|
| .mp4 | MP4 |
| .mkv | Matroska |
| .avi | AVI |
| .webm | WebM |
| .mov | QuickTime |

---

## Executando Processamento em Lote

### Comando Básico

```bash
python -m src.cli.commands process video.mp4 --batch ./pasta_videos
```

Nota: O `video.mp4` é opcional quando se usa `--batch`, mas é necessário para a CLI.

### Especificando a Pasta

```bash
python -m src.cli.commands process video.mp4 --batch ./videos
```

### Com Configuração

```bash
python -m src.cli.commands process video.mp4 \
  --batch ./videos \
  -c config.json
```

---

## Opções de Processamento em Lote

### Com Detecção de Cenas

```bash
python -m src.cli.commands process video.mp4 \
  --batch ./videos \
  --visual-cut
```

### Com Remoção de Silêncio

```bash
python -m src.cli.commands process video.mp4 \
  --batch ./videos \
  --remove-silence
```

### Completo

```bash
python -m src.cli.commands process video.mp4 \
  --batch ./videos \
  --visual-cut \
  --sensitivity high \
  --remove-silence \
  --normalize-audio \
  --generate-subtitles
```

---

## Arquivo de Configuração

Recomendamos usar um arquivo de configuração para lotes:

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
    },
    "normalization": {
      "enabled": true
    }
  },
  "subtitles": {
    "enabled": true,
    "format": "srt",
    "burn": false,
    "whisper_model": "tiny"
  },
  "output": {
    "format": "mp4",
    "quality": "high",
    "keep_original": true,
    "max_workers": 4
  }
}
```

**Nota:** Para lotes, use `whisper_model: "tiny"` para velocidade.

---

##Saída do Processamento em Lote

A saída mostra o progresso de cada vídeo:

```
Processando 5 vídeos...
✓ video1.mp4: 8 clips
✓ video2.mp4: 5 clips
✓ video3.mp4: 12 clips
✗ video4.mp4: Erro: Formato não suportado
✓ video5.mp4: 3 clips
```

### Legenda dos Símbolos

| Símbolo | Significado |
|---------|-----------|
| ✓ | Sucesso |
| ✗ | Erro |
| ! | Aviso |

---

## Estrutura de Pastas Gerada

```
pasta_videos/
├── video1.mp4/
│   ├── clips/
│   │   ├── clip_001.mp4
│   │   ├── clip_002.mp4
│   │   └── ...
│   └── report.json
├── video2.mp4/
│   ├── clips/
│   │   ├── clip_001.mp4
│   │   └── ...
│   └── report.json
└── ...
```

---

## Workers Paralelos

Para acelerar, use múltiplos workers:

```json
{
  "output": {
    "max_workers": 4
  }
}
```

| workers | Videos simultâneos | RAM necessária |
|---------|-------------------|---------------|
| 1 | 1 | 2 GB |
| 2 | 2 | 4 GB |
| 4 | 4 | 8 GB |
| 6 | 6 | 12 GB |

---

## Casos de Uso

### Cenário 1: Playlist do YouTube

Você tem uma playlist para fazer upload:

```bash
# Coloco todos os vídeos na pasta
mkdir ./youtube_videos
# Copie os vídeos para lá

# Execute o processamento
python -m src.cli.commands process video.mp4 \
  --batch ./youtube_videos \
  -c config_youtube.json
```

### Cenário 2: Games para TikTok

Múltiplas partidas para editar:

```bash
python -m src.cli.commands process video.mp4 \
  --batch ./games \
  --visual-cut \
  --sensitivity high \
  --remove-silence
```

### Cenário 3: Entrevistas

Múltiplas entrevistas:

```bash
python -m src.cli.commands process video.mp4 \
  --batch ./entrevistas \
  --visual-cut \
  --normalize-audio \
  --generate-subtitles
```

---

## Relatório de Lote

Ao final, um relatório Consolidado é gerado:

```json
{
  "batch_summary": {
    "total_videos": 10,
    "successful": 8,
    "failed": 2,
    "total_clips": 45,
    "total_duration": 720.5,
    "duration_removed": 45.2
  },
  "videos": [
    {
      "name": "video1.mp4",
      "status": "success",
      "clips": 8,
      "duration": 120.5
    },
    {
      "name": "video2.mp4",
      "status": "error",
      "error": "Formato não suportado"
    }
  ]
}
```

---

## Limitações

| Limitação | Valor |
|-----------|-------|
| Máximo de vídeos | 100 por lote |
| Máximo de workers | 8 |
| Tamanho máximo por vídeo | 10 GB |

---

## Dicas e Truques

### 1. Organize por Pasta

```
./processar/
├── youtube/
│   └── *.mp4
├── tiktok/
│   └── *.mp4
└── entrevistas/
    └── *.mp4
```

### 2. Use Prefixes

Para saber qual vídeo veio de onde:

```bash
# Processar cada pasta separadamente
python -m src.cli.commands process video.mp4 --batch ./youtube -c config_yt.json
python -m src.cli.commands process video.mp4 --batch ./tiktok -c config_tiktok.json
```

### 3. Use Modelo tiny

Para processamento rápido:

```json
{
  "subtitles": {
    "whisper_model": "tiny"
  }
}
```

### 4. Monitore

Para ver o progresso:

```bash
python -m src.cli.commands process video.mp4 --batch ./videos -v
```

---

## Próximos Passos

- **[Exemplos Práticos](../examples/index.md)** - Mais casos de uso
- **[Solução de Problemas](../troubleshooting.md)** - Erros comuns

---

## Suporte

Para problemas com processamento em lote, consulte a página de **[Solução de Problemas](../troubleshooting.md)**.

---

*Última atualização: 2026-04-29*