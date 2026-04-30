# Interface Gráfica (GUI)

A Interface Gráfica (GUI) do Video Clips Automation permite processar vídeos de forma visual, sem necessidade de digitar comandos.

## Visão Geral da GUI

A GUI oferece uma forma intuitiva de:

- Selecionar arquivos de vídeo
- Configurar opções de detecção
- Visualizar os pontos de corte em uma linha do tempo
- Assistir preview do vídeo
- Processar com um clique

### Requisitos

A interface gráfica requer PyQt6:

```bash
pip install PyQt6
```

---

## Abrindo a GUI

### Via Comando CLI

```bash
python -m src.cli.commands gui
```

### Via Python

```python
from src.gui.main_window import main
main()
```

---

## Componentes da Interface

A GUI é composta por várias áreas:

```
┌─────────────────────────────────────────────────────────────┐
│  Barra de Título                                         │
├─────────────────────────────────────────────────────────────┤
│  Menu: Arquivo | Editar | Visualizar | Ajuda              │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌───────────────────────────────┐  │
│  │                 │  │                               │  │
│  │  Seleção de    │  │      Janela de Preview        │  │
│  │  Vídeo         │  │      (Assistir vídeo)          │  │
│  │                 │  │                               │  │
│  └─────────────────┘  └───────────────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  Painel de Opções                                        │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ │ Detecção de Cena     [✓] Ativar                  │ │
│  │ │ Sensibilidade        [Média ▼]                   │ │
│  │ │ Remoção de Silêncio  [✓] Ativar                  │ │
│  │ │ Threshold (dB)      [-40 ______]                │ │
│  │ │ Normalizar Áudio     [ ] Ativar                 │ │
│  │ │ Gerar Legendas       [ ] Ativar                 │ │
│  └─────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  Linha do Tempo                                          │
│  [████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│ 1:23]   │
│     ↑↑ Clip 1                      ↑↑ Clip 2          │
├─────────────────────────────────────────────────────────────┤
│  [Preview]                          [Processar]         │
└─────────────────────────────────────────────────────────────┘
```

---

## Detalhes de Cada Componente

### 1. Seleção de Vídeo

Arraste um arquivo de vídeo para esta área ou clique para selecionar.

**Formatos suportados:**
- MP4 (.mp4)
- Matroska (.mkv)
- AVI (.avi)
- WebM (.webm)
- QuickTime (.mov)

**Limitações:**
- Tamanho máximo: 10GB
- O vídeo precisa ter áudio (ou marque a opção "Sem Áudio")

### 2. Janela de Preview

Exibe o vídeo selected enquanto você configura as opções.

**Controles:**
- Play/Pause (espaço)
- Avançar quadro (→)
- Voltar quadro (←)
- Volume (+/-)

### 3. Painel de Opções

| Opção | Descrição | Padrão |
|-------|-----------|--------|
| Detecção de Cena | Ativar detecção automática de cenas | Ativado |
| Sensibilidade | Quão sensível é a detecção | Média |
| Remoção de Silêncio | Remover trechos silenciosos | Desativado |
| Threshold (dB) | Nível de silêncio em dB | -40 |
| Duração Mínima | Duração mínima do silêncio | 0.5s |
| Normalizar Áudio | Equalizar volume | Desativado |
| Gerar Legendas | Criar legendas com IA | Desativado |
| Queimar Legendas | Inserir legendas no vídeo | Desativado |

### 4. Linha do Tempo

Visualização graphical dos clips detectados.

**Informações exibidas:**
- Duração total do vídeo
- Posição atual do playback
- Marcação dos clips detectados
- Código de cores por tipo de clip

---

## Fluxo de Trabalho na GUI

### Passo 1: Selecionar Vídeo

Clique na área de seleção ou arraste o arquivo de vídeo.

O vídeo começará a tocar no preview.

### Passo 2: Configurar Opções

Ajuste as opções no painel conforme sua necessidade:

- Ative ou desative detecção de cena
- Escolha a sensibilidade
- Configure remoção de silêncio (se necessário)
- Ative legendas (se desejado)

### Passo 3: Visualizar Clips

A linha do tempo mostrará onde os clips serão feitos.

Clique em um clip na linha do tempo para pular para aquela posição no vídeo.

### 4: Processar

Clique no botão "Processar" para iniciar.

Uma barra de progresso mostrará o andamento.

### Passo 5: Resultados

Quando concluído, uma notificação aparecerá.

Os clips serão salvos em uma pasta `clips/` ao lado do vídeo original.

---

## Atalhos de Teclado

| Tecla | Ação |
|-------|------|
| Espaço | Play/Pause |
| → | Próximo quadro |
| ← | Quadro anterior |
| ↑ | Aumentar volume |
| ↓ | Diminuir volume |
| Ctrl+O | Abrir arquivo |
| Ctrl+P | Preview |
| Enter | Processar |
| F5 | Atualizar |
| Esc | Sair |

---

## Configurações da GUI

### Tamanho da Janela

O tamanho padrão é 1200x800 pixels.

Para iniciar com tamanho diferente:

```python
from src.gui.main_window import main
main(width=1600, height=900)
```

### Tema

A GUI usa o tema do sistema operacional por padrão.

Para forçar um tema específico:

```bash
export QT_QPA_PLATFORMTHEME=gtk3
python -m src.cli.commands gui
```

---

## Diferenças Entre CLI e GUI

| Recurso | CLI | GUI |
|---------|-----|-----|
| Detecção de Cena | ✓ | ✓ |
| Remoção de Silêncio | ✓ | ✓ |
| Normalização | ✓ | ✓ |
| Legendas | ✓ | ✓ |
| Preview em Tempo Real | ✗ | ✓ |
| Linha do Tempo | ✗ | ✓ |
| Processamento em Lote | ✓ | ✗ |
| Automação/Scripts | ✓ | ✗ |

---

## Solução de Problemas da GUI

### GUI não abre

**Problema:** "Erro: PyQt6 não está instalado"

**Solução:**

```bash
pip install PyQt6
```

### Vídeo não carrega

**Verifique:**
1. O formato do arquivo é suportado
2. O arquivo não está corrompido
3. Não ultrapassa 10GB

### Preview não funciona

**Problema:** "Erro ao carregar vídeo"

**Solução:**
1. Verifique se o FFmpeg está instalado
2. Tente reproduzir o vídeo em outro player

---

## Próximos Passos

- **[Arquivo de Configuração](config.md)** - Configurações avançadas
- **[Detecção de Cenas](../features/scene-detection.md)** - Como funciona a detecção
- **[Exemplos Práticos](../examples/index.md)** - Casos de uso

---

## Suporte

Para problemas específicos da GUI, consulte a página de **[Solução de Problemas](../troubleshooting.md)**.

---

*Última atualização: 2026-04-29*