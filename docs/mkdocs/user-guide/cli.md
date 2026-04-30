# Interface CLI (Linha de Comando)

A Interface de Linha de Comando (CLI) é a forma mais flexível de usar o Video Clips Automation.Todos os comandos são executados via terminal.

## Visão Geral

A CLI oferece os seguintes comandos:

| Comando | Descrição |
|---------|-----------|
| `process` | Processa um vídeo e gera clips |
| `preview` | Mostra os pontos de corte sem processar |
| `init-config` | Cria um arquivo de configuração |
| `gui` | Abre a interface gráfica |

---

## Comando: process

O comando principal para processar vídeos e gerar clips automáticos.

### Sintaxe Básica

```bash
python -m src.cli.commands process <caminho_do_video> [OPÇÕES]
```

### Argumentos

| Argumento | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `video_path` | Sim | Caminho para o arquivo de vídeo |

### Opções

#### Opções de Detecção de Cenas

| Opção | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `--visual-cut` / `--no-visual-cut` | Flag | Ativado | Ativar/desativar detecção de cena |
| `--sensitivity` | Texto | medium | Sensibilidade: low, medium, high |

**Exemplo:**

```bash
python -m src.cli.commands process video.mp4 --visual-cut --sensitivity high
```

#### Opções de Remoção de Silêncio

| Opção | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `--remove-silence` | Flag | Desativado | Ativar remoção de silêncio |
| `--silence-db` | Número | -40 | Threshold em dB (mais negativo = mais sensível) |
| `--silence-duration` | Número | 0.5 | Duração mínima em segundos |

**Exemplos:**

```bash
# Remover silêncio com threshold padrão
python -m src.cli.commands process video.mp4 --remove-silence

# Threshold personalizado (-50dB é mais sensível)
python -m src.cli.commands process video.mp4 --remove-silence --silence-db -50

# Duração mínima de 2 segundos
python -m src.cli.commands process video.mp4 --remove-silence --silence-duration 2.0
```

#### Opções de Áudio

| Opção | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `--normalize-audio` | Flag | Desativado | Normalizar volume do áudio |
| `--no-audio` | Flag | Desativado | Indicar que o vídeo não tem áudio |

**Exemplo:**

```bash
python -m src.cli.commands process video.mp4 --normalize-audio
```

#### Opções de Legendas

| Opção | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `--generate-subtitles` | Flag | Desativado | Gerar legendas automáticas |
| `--export-subtitles` | Texto | srt | Formato: srt ou vtt |
| `--burn-subtitles` | Flag | Desativado | Queimar legendas no vídeo |

**Exemplos:**

```bash
# Gerar legendas em formato SRT
python -m src.cli.commands process video.mp4 --generate-subtitles

# Gerar legendas em formato VTT
python -m src.cli.commands process video.mp4 --generate-subtitles --export-subtitles vtt

# Queimar legendas no vídeo
python -m src.cli.commands process video.mp4 --generate-subtitles --burn-subtitles
```

#### Opções de Saída

| Opção | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `--output-dir`, `-o` | Texto | Automaticamente | Diretório de saída |
| `--destroy` | Flag | Desativado | Excluir arquivo original após processar |
| `--config`, `-c` | Texto | - | Arquivo de configuração JSON |
| `--batch`, `-b` | Texto | - | Processar todos os vídeos da pasta |
| `--min-clip-duration` | Número | 0.0 | Duração mínima - apenas clips MAIORES que este valor (ex: 5 = clips com mais de 5s) |
| `--verbose`, `-v` | Flag | Desativado | Log verboso |

**Exemplos:**

```bash
# Definir diretório de saída
python -m src.cli.commands process video.mp4 -o ./meus_clips

# Excluir original após processamento
python -m src.cli.commands process video.mp4 --destroy

# Usar arquivo de configuração
python -m src.cli.commands process video.mp4 -c minha_config.json

# Processar todos os vídeos de uma pasta
python -m src.cli.commands process video.mp4 --batch ./videos

# Log verboso para debug
python -m src.cli.commands process video.mp4 -v
```

---

## Comando: preview

Visualiza os pontos de corte detectados sem processar o vídeo.

### Sintaxe

```bash
python -m src.cli.commands preview <caminho_do_video> [OPÇÕES]
```

### Opções

| Opção | Tipo | Descrição |
|-------|------|-----------|
| `--output-dir`, `-o` | Texto | Diretório de saída |
| `--json` | Texto | Salvar resultado em arquivo JSON |

### Exemplo

```bash
python -m src.cli.commands preview video.mp4
```

**Saída:**

```
Pontos de corte detectados:
  1: 00:00.00s - 00:02.30s (scene_change)
  2: 00:02.30s - 00:05.15s (scene_change)
  3: 00:05.15s - 00:08.42s (scene_change)
Total: 3 clips
```

### Salvar em JSON

```bash
python -m src.cli.commands preview video.mp4 --json pontos.json
```

---

## Comando: init-config

Cria um arquivo de configuração de exemplo.

### Sintaxe

```bash
python -m src.cli.commands init-config [OPÇÕES]
```

### Opções

| Opção | Tipo | Descrição |
|-------|------|-----------|
| `--output`, `-o` | Texto | Caminho do arquivo de saída |

### Exemplo

```bash
python -m src.cli.commands init-config
```

**Saída:**

```
Configuração salva em: config.example.json
```

### Com caminho personalizado

```bash
python -m src.cli.commands init-config -o ./config/minha_config.json
```

---

## Comando: gui

Abre a interface gráfica (GUI).

### Sintaxe

```bash
python -m src.cli.commands gui
```

### Requisitos

A GUI requer PyQt6 instalado. Se não estiver instalado:

```bash
pip install PyQt6
```

---

## Guia de Uso por Cenário

### Cenário 1: Criar Clips para Redes Sociais

Para YouTube, TikTok ou Instagram:

```bash
python -m src.cli.commands process video.mp4 --visual-cut --sensitivity high
```

### Cenário 2: Remover Pausas e Silêncios

Para remover silêncio de apresentações:

```bash
python -m src.cli.commands process video.mp4 --remove-silence --silence-db -45 --silence-duration 1.0
```

### Cenário 3: Criar Clips com Legendas

Para videos com legendas automáticas:

```bash
python -m src.cli.commands process video.mp4 --generate-subtitles --burn-subtitles
```

### Cenário 4: Processamento em Lote

Para processar vários vídeos:

```bash
python -m src.cli.commands process video.mp4 --batch ./videos
```

---

## Opções Combinadas

Você pode combinar várias opções em um único comando:

```bash
python -m src.cli.commands process video.mp4 \
  --visual-cut \
  --sensitivity high \
  --remove-silence \
  --silence-db -40 \
  --normalize-audio \
  --generate-subtitles \
  --burn-subtitles \
  -o ./output \
  -v
```

---

## Variáveis de Ambiente

Algumas opções podem ser definidas via variáveis de ambiente:

| Variável | Descrição |
|----------|-----------|
| `FFMPEG_PATH` | Caminho do executável FFmpeg |
| `LOG_LEVEL` | Nível de log: DEBUG, INFO, WARNING, ERROR |
| `MAX_WORKERS` | Número máximo de workers para processamento |

**Exemplo:**

```bash
export LOG_LEVEL=DEBUG
python -m src.cli.commands process video.mp4
```

---

## Atalhos Úteis

### Ver Ajuda Completa

```bash
python -m src.cli.commands process --help
python -m src.cli.commands preview --help
```

### Ver Versão

```bash
python -m src.cli.commands --version
```

### Listar Todos os Comandos

```bash
python -m src.cli.commands --help
```

---

## Códigos de Saída

A CLI retorna códigos de saída para indicar o resultado:

| Código | Significado |
|--------|-------------|
| 0 | Sucesso |
| 1 | Erro genérico |
| 2 | Erro de argumento |
| 3 | Erro de arquivo não encontrado |
| 4 | Erro de FFmpeg |

---

## Próximos Passos

- **[Interface GUI](gui.md)** - Interface gráfica
- **[Arquivo de Configuração](config.md)** - Configurações avançadas
- **[Exemplos Práticos](../examples/index.md)** - Mais casos de uso

---

## Suporte

Para problemas, consulte a página de **[Solução de Problemas](../troubleshooting.md)**.

---

*Última atualização: 2026-04-29*