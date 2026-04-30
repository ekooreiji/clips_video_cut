# Detecção de Cenas

A detecção de cenas é o recurso principal do Video Clips Automation. Ele identifica automaticamente onde uma cena termina e outra começa no vídeo.

## Como Funciona

O sistema usa análise de visão computacional para comparar quadros consecutivos do vídeo:

1. **Extração de Quadros** - O vídeo é dividido em quadros (frames) individuais
2. **Análise de Diferença** - Cada quadro é comparado com o anterior
3. **Cálculo de Score** - Um score de "diferença visual" é calculado
4. **Detecção de Transição** - Quando o score ultrapassa um limite, uma nova cena é detectada

```
Quadro 1 ████████████████████████
Quadro 2 ████████████████████████  Diferença: 5%
Quadro 3 ████████░░░░░█████████  Diferença: 45% ← Nova cena detectada!
Quadro 4 ████████░░░░░█████████
```

---

## Sensibilidade

A sensibilidade determina quão grande precisa ser a diferença visual para detectar uma nova cena.

### Níveis de Sensibilidade

| Nível | Valor | Melhor para |
|--------|-------|-----------|
| Baixa | 0.3 | Vídeos com mudanças subtis |
| Média | 1.0 | Uso geral (padrão) |
| Alta | 2.0 | Vídeos com mudanças drásticas |

### Escolhendo a Sensibilidade Certa

**Alta sensibilidade (baixo valor):**
- Produz mais clips
- Para vídeos com mudanças de cena sutis
- Cenas com movimento gradual
- Transições de câmera lentas

**Baixa sensibilidade (alto valor):**
- Produz menos clips
- Para vídeos com muita ação
- Games com explosões
- Movimentos rápidos de câmera

---

## Opções de Configuração

### Via CLI

```bash
# Sensibilidade média (padrão)
python -m src.cli.commands process video.mp4 --visual-cut

# Sensibilidade alta (mais clips)
python -m src.cli.commands process video.mp4 --sensitivity high

# Sensibilidade baixa (menos clips)
python -m src.cli.commands process video.mp4 --sensitivity low
```

### Via Arquivo de Configuração

```json
{
  "processing": {
    "visual_cut": {
      "enabled": true,
      "sensitivity": 1.5,
      "sample_rate": 5
    }
  }
}
```

### Parâmetros Avançados

| Parâmetro | Descrição | Padrão |
|-----------|-----------|-------|
| `sensitivity` | Fator multiplicativo do threshold | 1.0 |
| `sample_rate` | Analisar a cada N quadros | 5 |

---

## Taxa de Amostragem

O parâmetro `sample_rate` determina com que frequência os quadros são analisados:

- **sample_rate = 1**: Analisa todos os quadros (mais preciso, mais lento)
- **sample_rate = 5**: Analisa a cada 5 quadros (equilibrado)
- **sample_rate = 10**: Analisa a cada 10 quadros (mais rápido, menos preciso)

Para vídeos em 30fps:
- sample_rate 5 = 6 análises por segundo
- sample_rate 10 = 3 análises por segundo

---

## Exemplo Prático

### Cenário: Tutorial em Vídeo

Você gravou um tutorial com 3 assuntos diferentes:

1. Introdução (0:00 - 2:00)
2. Assunto 1 (2:00 - 5:00)
3. Assunto 2 (5:00 - 8:00)

**Comando:**

```bash
python -m src.cli.commands process tutorial.mp4 --visual-cut --sensitivity medium
```

**Resultado:**

```
Clip 1: 00:00 - 02:00 (intro)
Clip 2: 02:00 - 05:00 (assunto 1)
Clip 3: 05:00 - 08:00 (assunto 2)
```

### Cenário: Gameplay

Você gravou um gameplay com várias partidas:

**Comando:**

```bash
python -m src.cli.commands process gameplay.mp4 --visual-cut --sensitivity high --sample-rate 3
```

**Por que high?**
- Mudanças de cena claras entre rounds
- Tela de loading entre partidas
- Menu de pausa

---

## Limitações

A detecção de cena não funciona bem em alguns cenários:

| Cenário | Problema | Solução |
|---------|---------|--------|
| Transições suaves | Não detecta | Use sensibilidade alta |
| Vídeo muito escuro | Falsos positivos | Ajuste threshold manualmente |
| Muito movimento | Muitos clips | Use sensibilidade baixa |
| Slides/PPT | Não detecta | Corte manualmente |

---

## Métricas de Output

Após o processamento, você recebe um relatório:

```json
{
  "clips_detected": 8,
  "clips": [
    {
      "id": 1,
      "start_time": 0.0,
      "end_time": 145.2,
      "duration": 145.2,
      "reason": "scene_change",
      "scene_score": 0.85
    }
  ]
}
```

### Entendendo os Scores

| Campo | Descrição |
|-------|---------|
| `scene_score` | Score de mudança (0-1) |
| `threshold_low` | Threshold inferior |
| `threshold_high` | Threshold superior |

O `scene_score` indica quão "forte" foi a mudança de cena:
- 0.0-0.3: Mudança fraca
- 0.3-0.7: Mudança moderada
- 0.7-1.0: Mudança forte

---

## Dicas e Truques

### 1. Use Preview Primeiro

Sempre rode o preview antes do processamento real:

```bash
python -m src.cli.commands preview video.mp4
```

### 2. Ajuste a Sensibilidade

Se houver muitos clips, diminua a sensibilidade:

```bash
python -m src.cli.commands process video.mp4 --sensitivity low
```

Se houver poucos clips, aumente:

```bash
python -m src.cli.commands process video.mp4 --sensitivity high
```

### 3. Combine Com Remoção de Silêncio

Para melhores resultados:

```bash
python -m src.cli.commands process video.mp4 \
  --visual-cut \
  --remove-silence \
  --silence-db -40
```

---

## Comparação com Outros Métodos

| Método | Precisão | Velocidade | Adequado para |
|--------|---------|-----------|-----------|
| Detecção de Cena | Boa | Rápido | Uso geral |
| Detecção de Áudio | Muito boa | Médio | Videos com fala |
| Combinação | Excelente | Lento | Melhor resultado |

---

## Próximos Passos

Agora que você entende a detecção de cenas:

- **[Remoção de Silêncio](silence-removal.md)** - Remova trechos silenciosos
- **[Legendas](subtitles.md)** - Adicione legendas
- **[Exemplos Práticos](../examples/index.md)** - Mais casos

---

## Suporte

Para problemas, veja **[Solução de Problemas](../troubleshooting.md)**.

---

*Última atualização: 2026-04-29*