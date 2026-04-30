# Legendas Automáticas

O Video Clips Automation pode gerar legendas automáticas usando inteligência artificial através do Whisper.

## Como Funciona

O sistema usa o modelo Whisper da OpenAI para transcrever o áudio do vídeo:

1. **Extração de Áudio** - O áudio é extraído do vídeo
2. **Transcrição** - O Whisper transcreve o áudio para texto
3. **Sincronização** - Os timestamps são sincronizados
4. **Geração** - Arquivo de legendas é criado (SRT ou VTT)

```
Áudio: "Olá, bem-vindos ao tutorial..."
         ↓
Whisper: "Olá, bem-vindos ao tutorial..."
         ↓
Legenda: 00:00:01 --> 00:00:04
         Olá, bem-vendios ao tutorial...
```

---

## Modelos Whisper

Você pode escolher entre diferentes modelos:

| Modelo | Tamanho | Velocidade | Precisão |
|---------|---------|-----------|----------|
| tiny | 39 MB | Muito rápida | Boa |
| base | 74 MB | Rápida | Muito boa |
| small | 244 MB | Média | Excelente |
| medium | 769 MB | Lenta | Excelente |
| large | 1550 MB | Muito lenta | Melhor |

### Recomendação

- **tiny**: Para pré-visualização ou vídeos curtos
- **base**: Para uso geral (padrão)
- **small**: Para mejor precisão recomendada
- **medium/large**: Para precisão máxima

---

## Formatos de Legenda

### SRT (SubRip Text)

Formato mais comum, suportado por todos os players:

```srt
1
00:00:01,000 --> 00:00:04,000
Olá, bem-vindos ao tutorial

2
00:00:04,500 --> 00:00:07,200
Hoje vamos aprender sobre...
```

### VTT (WebVTT)

Formato web, ideal para HTML5:

```vtt
WEBVTT

00:00:01.000 --> 00:00:04.000
Olá, bem-vindos ao tutorial

00:00:04.500 --> 00:00:07.200
Hoje vamos aprender sobre...
```

---

## Opções de Uso

### Gerar Legendas SRT

```bash
python -m src.cli.commands process video.mp4 --generate-subtitles
```

### Gerar Legendas VTT

```bash
python -m src.cli.commands process video.mp4 \
  --generate-subtitles \
  --export-subtitles vtt
```

### Queimar Legendas no Vídeo

```bash
python -m src.cli.commands process video.mp4 \
  --generate-subtitles \
  --burn-subtitles
```

### Usar Modelo Diferente

```bash
python -m src.cli.commands process video.mp4 \
  --generate-subtitles
# Ou configure no arquivo de configuração:
```

```json
{
  "subtitles": {
    "enabled": true,
    "format": "srt",
    "burn": true,
    "whisper_model": "small"
  }
}
```

---

## Via Arquivo de Configuração

```json
{
  "subtitles": {
    "enabled": true,
    "format": "srt",
    "burn": false,
    "whisper_model": "base"
  }
}
```

---

## Casos de Uso

### YouTube

Para fazer upload no YouTube:

```bash
python -m src.cli.commands process video.mp4 \
  --generate-subtitles \
  --export-subtitles srt
```

### Web (HTML5)

Para embed em site:

```bash
python -m src.cli.commands process video.mp4 \
  --generate-subtitles \
  --export-subtitles vtt
```

### TikTok/Instagram

Para redes sociais (legendas queimadas):

```bash
python -m src.cli.commands process video.mp4 \
  --generate-subtitles \
  --burn-subtitles
```

### Stories

Para stories com legendas:

```bash
python -m src.cli.commands process video.mp4 \
  --generate-subtitles \
  --burn-subtitles \
  --sensitivity high
```

---

## Idiomas

O Whisper detecta automaticamente o idioma. Para melhor precisão, especifique:

```python
# No arquivo de configuração
{
  "subtitles": {
    "language": "pt"
  }
}
```

Idios suportados incluem:
- Portuguese (pt)
- English (en)
- Spanish (es)
- French (fr)
- German (de)
- E muitos outros...

---

## Limitações

| Cenário | Problema | Solução |
|---------|---------|--------|
| Áudio ruim | Transcrição imprecisa | Limpe o áudio primeiro |
| Múltiplos falantes | Não diferencia | Edite manualmente |
| Música apenas | Não transcreve | Use sem --generate |
| Línguas mistas | Mistura resultados | Especifique idioma |

---

## Arquivos Gerados

Quando você gera legendas, os seguintes arquivos são criados:

```
video.mp4/
├── clips/
│   ├── clip_001.mp4
│   └── ...
├── video.srt          ← Legendas
└── report.json
```

Se `--burn-subtitles` for usado:

```
video.mp4/
├── clips/
│   ├── clip_001.mp4    ← Com legendas
│   └── ...
└── report.json
```

---

## Editando Legendas

Após gerar, você pode editar o arquivo de legendas:

### SRT

Abra em qualquer editor de texto:

```srt
1
00:00:01,000 --> 00:00:04,000
Olá, bem-vindos ao tutorial DE WIDGET
```

### VTT

```vtt
00:00:01.000 --> 00:00:04.000
Olá, bem-vindos ao tutorial
```

---

## Dicas e Truques

### 1. Velocidade

Use o modelo "tiny" para testes:

```bash
# Configuração rápida
{
  "subtitles": {
    "whisper_model": "tiny"
  }
}
```

### 2. Precisão

Use "small" ou "medium":

```bash
# Configuração de precisão
{
  "subtitles": {
    "whisper_model": "small"
  }
}
```

### 3. Queimar Legendas

O processamento leva mais tempo, mas o resultado é embedado:

```bash
python -m src.cli.commands process video.mp4 \
  --generate-subtitles \
  --burn-subtitles
```

---

## Formato de Output

O relatório inclui informações sobre as legendas:

```json
{
  "subtitles": {
    "generated": true,
    "format": "srt",
    "burned": false,
    "language": "pt",
    "model": "base",
    "duration": 145.2,
    "words": 523
  }
}
```

---

## Próximos Passos

- **[Processamento em Lote](batch-processing.md)** - Processe vários vídeos
- **[Exemplos Práticos](../examples/index.md)** - Mais casos
- **[Interface CLI](../user-guide/cli.md)** - Todos os comandos

---

## Suporte

Para problemas, consulte a página de **[Solução de Problemas](../troubleshooting.md)**.

---

*Última atualização: 2026-04-29*