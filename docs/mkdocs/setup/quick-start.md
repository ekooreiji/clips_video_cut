# Guia Rápido

Este guia mostra como processar seu primeiro vídeo em menos de 5 minutos. Vamos lá!

## O Que Você Precisa

Antes de começar, tenha em mãos:

1. Um arquivo de vídeo (MP4, MKV, AVI, WebM ou MOV)
2. O Video Clips Automation instalado (veja a página de [Instalação](installation.md))
3. Acesso ao terminal ou prompt de comando

---

## Passo 1: Ative o Ambiente Virtual

Se você criou um ambiente virtual, ative-o agora:

**Windows:**

```bash
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

---

## Passo 2: Processe Seu Primeiro Vídeo

Agora, execute o comando mais básico:

```bash
python -m src.cli.commands process seu_video.mp4
```

Substitua `seu_video.mp4` pelo nome do seu arquivo de vídeo.

### O Que Acontece?

O sistema vai:

1. **Analisar o vídeo** - Ler todos os quadros e detectar mudanças de cena
2. **Identificar os clips** - Encontrar onde cada cena começa e termina
3. **Salvar os clips** - Criar arquivos individuais na pasta `seu_video.mp4/clips/`
4. **Gerar relatório** - Criar um arquivo JSON com informações sobre cada clip

### Saída Típica

```
Video: seu_video.mp4
Clips detectados: 8
Arquivo de relatório: seu_video.mp4/clips/report.json
```

---

## Passo 3: Visualize os Resultados

Abra a pasta criada para ver os clips:

```
seu_video.mp4/
├── clips/
│   ├── clip_001.mp4
│   ├── clip_002.mp4
│   ├── clip_003.mp4
│   └── ...
└── report.json
```

Cada clip é um arquivo单独的 de vídeo com uma cena diferente.

---

## Exemplos de Comandos

Aqui estão alguns exemplos práticos para diferentes situações:

### Exemplo 1: Detecção de Cenas

Para detectar automaticamente as mudanças de cena:

```bash
python -m src.cli.commands process video.mp4 --visual-cut
```

Este é o comportamento padrão, então 也可以 apenas:

```bash
python -m src.cli.commands process video.mp4
```

### Exemplo 2: Remoção de Silêncio

Para remover partes silenciosas do vídeo:

```bash
python -m src.cli.commands process video.mp4 --remove-silence
```

### Exemplo 3: Com Sensibilidade Diferente

Para vídeos com mudanças de cena sutis, use sensibilidade alta:

```bash
python -m src.cli.commands process video.mp4 --sensitivity high
```

Para vídeos com muitas mudanças,use baixa:

```bash
python -m src.cli.commands process video.mp4 --sensitivity low
```

### Exemplo 4: geração de Legendas

Para gerar legendas automáticas:

```bash
python -m src.cli.commands process video.mp4 --generate-subtitles
```

Para queimar as legendas no vídeo:

```bash
python -m src.cli.commands process video.mp4 --generate-subtitles --burn-subtitles
```

### Exemplo 5: Pasta de Saída Personalizada

Para definir onde os clips serão salvos:

```bash
python -m src.cli.commands process video.mp4 -o ./meus_clips
```

---

## Usando o Preview

Antes de processar, você pode visualizar onde os clips serão cortados:

```bash
python -m src.cli.commands preview video.mp4
```

Você verá uma lista com todos os pontos de corte detectados:

```
Pontos de corte detectados:
  1: 00:00.00s - 00:02.30s (scene_change)
  2: 00:02.30s - 00:05.15s (scene_change)
  3: 00:05.15s - 00:08.42s (scene_change)
Total: 3 clips
```

Isso é útil para ajustar os parâmetros antes do processamento real.

---

## Usando Arquivo de Configuração

Se você usa as mesmas opções sempre, crie um arquivo de configuração:

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

Salve como `config.json` e use:

```bash
python -m src.cli.commands process video.mp4 -c config.json
```

---

## Fluxo de Trabalho Recomendado

Para obter os melhores resultados, siga estos passos:

1. **Preview primeiro** - Execute o preview para ver os pontos detectados
2. **Ajuste parâmetros** - Modifique sensibilidade ou threshold se necessário
3. **Processe** - Execute o processamento com os parâmetros ajustados
4. **Revise os clips** - Verifique os clips gerados
5. **Repita se necessário** - Ajuste e reprocesse

---

## Dica: Atalhos Úteis

### Ver Ajuda

```bash
python -m src.cli.commands process --help
```

### Ver Versão

```bash
python -m src.cli.commands --version
```

### Ativar Log Verboso

Para ver todos os detalhes do processamento:

```bash
python -m src.cli.commands process video.mp4 -v
```

---

## Próximos Passos

Agora que você fez seu primeiro processamento, explore mais:

- **[Interface CLI](../user-guide/cli.md)** - Todos os comandos disponíveis
- **[Interface GUI](../user-guide/gui.md)** - Interface gráfica
- **[Funcionalidades](../features/scene-detection.md)** - Detalhes de cada recurso
- **[Exemplos Práticos](../examples/index.md)** - Mais casos de uso

---

## Precisa de Ajuda?

Se algo não funcionou, veja a página de **[Solução de Problemas](../troubleshooting.md)**.

---

*Última atualização: 2026-04-29*