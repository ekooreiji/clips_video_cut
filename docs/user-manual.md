# Manual do Usuário - Video Clips Automation

| Metadata | Valor |
|----------|-------|
| **Versão** | 1.0.1 |
| **Data** | 2026-04-29 |

---

## Table of Contents

1. [Introdução](#1-introdução)
2. [Instalação](#2-instalação)
3. [Guia Rápido](#3-guia-rápido)
4. [Uso da CLI](#4-uso-da-cli)
5. [Uso da GUI](#5-uso-da-gui)
6. [Configuração](#6-configuração)
7. [Solução de Problemas](#7-solução-de-problemas)
8. [FAQ](#8-faq)

---

## 1. Introdução

### 1.1 O que é o Video Clips Automation?

O Video Clips Automation é uma ferramenta que ajuda você a cortar vídeos automaticamente com base na detecção de cenas e remoção de silêncio. É perfeito para criadores de conteúdo que desejam gerar clips para redes sociais rapidamente.

### 1.2 Funcionalidades

| Funcionalidade | Descrição |
|----------------|-----------|
| **Detecção de Cenas** | Detecta automaticamente mudanças de cena nos vídeos |
| **Remoção de Silêncio** | Remove partes silenciosas dos vídeos |
| **Normalização de Áudio** | Normaliza o volume do áudio |
| **Geração de Legendas** | Gera legendas usando IA Whisper |
| **Processamento em Lote** | Processa múltiplos vídeos de uma vez |
| **CLI e GUI** | Interfaces de linha de comando e gráfica |

---

## 2. Instalação

### 2.1 Pré-requisitos

- Python 3.10 ou superior
- FFmpeg (para processamento de vídeo)

### 2.2 Dependências do Projeto

| Pacote | Descrição |
|--------|-----------|
| **CLI** | |
| click | Interface de linha de comando |
| **GUI** | |
| PyQt6 | Interface gráfica |
| **Processamento de Vídeo** | |
| opencv-python | Visão computacional |
| imageio | Manipulação de imagens |
| imageio-ffmpeg | Suporte FFmpeg |
| ffmpeg-python | Interface FFmpeg |
| **Processamento de Áudio** | |
| scipy | Processamento científico |
| **Machine Learning** | |
| openai-whisper | Transcrição de áudio |
| torch | Framework ML |
| tiktoken | Tokenização |
| numba | Compilação JIT |
| **Numeração** | |
| numpy | Cálculos numéricos |
| **Testes** | |
| pytest | Framework de testes |
| pytest-cov | Cobertura de testes |
| pytest-asyncio | Testes async |
| **Utilitários** | |
| tqdm | Barra de progresso |
| python-dateutil | Utilitários de data |
| colorama | Cores no terminal |
| PyYAML | Configuração YAML |

### 2.3 Passos de Instalação

1. **Clone ou baixe o projeto:**
   ```bash
   git clone https://github.com/user/clips_videos.git
   cd clips_videos
   ```

2. **Crie um ambiente virtual:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate.bat  # Windows
   # source .venv/bin/activate  # Linux/Mac
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Instale o FFmpeg:**
   - **Windows:** Baixe em https://ffmpeg.org/download.html
   - **Mac:** `brew install ffmpeg`
   - **Linux:** `sudo apt install ffmpeg`

### 2.4 Verificação da Instalação

```bash
python -m src.cli.commands --version
```

Você deverá ver:
```
Video Clips Automation, version 1.0.0
```

---

## 3. Guia Rápido

### 3.1 Uso Básico - Detectar Cenas

```bash
python -m src.cli.commands process meuvideo.mp4
```

Isso irá:
1. Analisar o vídeo para mudanças de cena
2. Detectar 8 clips automaticamente
3. Salvar os clips na pasta `meuvideo.mp4/clips/`

### 3.2 Com Remoção de Silêncio

```bash
python -m src.cli.commands process meuvideo.mp4 --remove-silence
```

### 3.3 Processamento em Lote

```bash
python -m src.cli.commands process meuvideo.mp4 --batch ./videos
```

---

## 4. Uso da CLI

### 4.1 Comando Process

O comando principal para processar vídeos.

```bash
python -m src.cli.commands process <caminho_video> [OPÇÕES]
```

#### Opções

| Opção | Descrição | Exemplo |
|-------|------------|---------|
| `--visual-cut` | Ativar detecção de cena | `--visual-cut` |
| `--sensitivity` | Sensibilidade da detecção | `--sensitivity high` |
| `--min-clip-duration` | Duração mínima do clip (ex: 4s = clips com mais de 4 segundos) | `--min-clip-duration 4` |
| `--remove-silence` | Remover silêncio | `--remove-silence` |
| `--silence-db` | Threshold de silêncio (dB) | `--silence-db -50` |
| `--silence-duration` | Duração mínima do silêncio (s) | `--silence-duration 1.0` |
| `--normalize-audio` | Normalizar áudio | `--normalize-audio` |
| `--generate-subtitles` | Gerar legendas | `--generate-subtitles` |
| `--export-subtitles` | Formato das legendas | `--export-subtitles srt` |
| `--burn-subtitles` | Queimar legendas no vídeo | `--burn-subtitles` |
| `--destroy` | Excluir original após processar | `--destroy` |
| `--config` | Arquivo de configuração | `--config minha config.json` |
| `--batch` | Processar todos os vídeos da pasta | `--batch ./videos` |
| `-v, --verbose` | Log verboso | `-v` |

### 4.2 Comando Preview

Visualiza os pontos de corte detectados sem processar.

```bash
python -m src.cli.commands preview <caminho_video>
```

### 4.3 Comando Init Config

Cria um arquivo de configuração.

```bash
python -m src.cli.commands init-config
```

### 4.4 Comando GUI

Abre a interface gráfica.

```bash
python -m src.cli.commands gui
```

---

## 5. Uso da GUI

### 5.1 Abrindo a GUI

```bash
python -m src.cli.commands gui
```

### 5.2 Visão Geral da Interface

A GUI inclui:

- **Seleção de Vídeo**: Clique para selecionar um arquivo de vídeo
- **Painel de Opções**: Configure as opções de detecção e processamento
- **Linha do Tempo**: Visualização prévia dos pontos de clip
- **Janela de Preview**: Assista ao preview do vídeo
- **Botão Processar**: Inicie o processamento

### 5.3 Principais Funcionalidades

| Funcionalidade | Localização | Descrição |
|----------------|--------------|------------|
| Selecionar Vídeo | Janela principal | Clique para selecionar o arquivo de vídeo |
| Detecção de Cena | Painel de opções | Ativar/desativar detecção de cena |
| Sensibilidade | Painel de opções | Definir baixa/média/alta |
| Remoção de Silêncio | Painel de opções | Ativar remoção de silêncio |
| Preview | Janela principal | Ver os clips detectados |
| Processar | Janela principal | Iniciar o processamento |

---

## 6. Configuração

### 6.1 Formato do Arquivo de Configuração

Crie um arquivo JSON com suas configurações:

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
    }
  },
  "subtitles": {
    "enabled": false,
    "format": "srt",
    "burn": false
  },
  "output": {
    "keep_original": true,
    "max_workers": 3
  }
}
```

### 6.2 Usando a Configuração

```bash
python -m src.cli.commands process video.mp4 --config minhaconfig.json
```

---

## 7. Solução de Problemas

### 7.1 Problemas Comuns

| Problema | Causa | Solução |
|----------|-------|----------|
| FFmpeg não encontrado | FFmpeg não instalado ou não está no PATH | Instale o FFmpeg |
| Nenhum clip detectado | Vídeo não tem mudanças de cena | Tente sensibilidade mais baixa |
| Memória insuficiente | Vídeo muito grande | Processe vídeos menores |
| Erro ao processar | Vídeo corrompido | Use um vídeo diferente |

### 7.2 Mensagens de Erro

| Erro | Significado | Solução |
|------|--------------|----------|
| `FFmpeg não encontrado` | FFmpeg não instalado | Instale o FFmpeg |
| `Vídeo não encontrado` | Arquivo não encontrado | Verifique o caminho do arquivo |
| `Formato não suportado` | Formato não suportado | Use MP4, MKV, AVI, etc. |

---

## 8. FAQ

### 8.1 Perguntas Gerais

**P: Quais formatos de vídeo são suportados?**
R: MP4, MKV, AVI, WebM, MOV

**P: Como processar múltiplos vídeos de uma vez?**
R: Use a opção `--batch`:
```bash
python -m src.cli.commands process video.mp4 --batch ./videos
```

**P: Onde os clips são salvos?**
R: Em uma pasta `clips/` ao lado do vídeo original

### 8.2 Perguntas Técnicas

**P: O que é detecção de cena?**
R: A detecção de cena usa visão computacional para identificar mudanças entre quadros em um vídeo. Quando a diferença visual excede um limite, é detectada como uma nova cena/clip.

**P: Como funciona a remoção de silêncio?**
R: A ferramenta analisa a faixa de áudio e remove seções onde o nível de áudio está abaixo do limite especificado (padrão: -40dB).

**P: Posso usar meu próprio modelo Whisper?**
R: Sim, especifique com `--whisper_model` na config. Opções: tiny, base, small, medium

### 8.3 Ajuda

Para mais ajuda, execute:
```bash
python -m src.cli.commands --help
```

---

*Manual do Usuário - Video Clips Automation v1.0.0*