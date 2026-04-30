# Remoção de Silêncio

A remoção de silêncio detecta e remove automaticamente trechos do vídeo onde não há áudio relevante.

## Como Funciona

O sistema analisa a faixa de áudio do vídeo:

1. **Extração de Áudio** - O áudio é extraído do vídeo
2. **Análise de Amplitude** - Cada segmento é analisado quanto ao volume
3. **Detecção de Silêncio** - Trechos abaixo do threshold são identificados
4. **Corte e União** - Os clips são unidos, pulando ossilenciosos

```
Áudio: ▓▓▓▓▓▓░░░░▓▓▓▓▓▓░░░░▓▓▓▓▓▓
         ▓ Som    ░ Silêncio    ▓ Som
         
Resultado: ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
         (silêncio removido)
```

---

## Configuração

### Parâmetros Principais

| Parâmetro | Descrição | Padrão |
|-----------|-----------|-------|
| `db_threshold` | Nível em dB para considerar silêncio | -40 |
| `min_duration` | Duração mínima do silêncio em segundos | 0.5 |

### Threshold de dB

O threshold determina quão baixo o volume precisa estar para ser considerado silêncio:

| Threshold | Sensibilidade | Uso recomendado |
|-----------|-------------|--------------|
| -30 dB | Baixa | Áudio muito alto |
| -40 dB | Média | Uso geral |
| -50 dB | Alta | Áudio muito baixo |
| -60 dB | Muito alta |Áudio quase imperceptível |

**Entendendo dB:**

- 0 dB = Volume máximo
- -40 dB = Volume moderado (conversa normal)
- -60 dB = Volume muito baixo (sussurro)
- -80 dB = Quase silencioso

### Duração Mínima

A duração mínima evita que pequenos ruídos sejam removidos:

| Duração | Efeito |
|---------|--------|
| 0.3s | Remove pequenas pausas |
| 0.5s | Padrão recomendado |
| 1.0s | Remove pausas curtas |
| 2.0s | Only removes silenciosos longos |

---

## Exemplos de Uso

### Exemplo 1: Configuração Padrão

```bash
python -m src.cli.commands process video.mp4 --remove-silence
```

Remove trechos onde o áudio está abaixo de -40dB por mais de 0.5 segundos.

### Exemplo 2: Threshold Personalizado

```bash
python -m src.cli.commands process video.mp4 \
  --remove-silence \
  --silence-db -45
```

Remove trechos abaixo de -45dB (mais sensível).

### Exemplo 3: Duração Mínima

```bash
python -m src.cli.commands process video.mp4 \
  --remove-silence \
  --silence-duration 1.0
```

Only remove silêncio com mais de 1 segundo.

---

## Via Arquivo de Configuração

```json
{
  "processing": {
    "silence_removal": {
      "enabled": true,
      "db_threshold": -40,
      "min_duration": 0.5
    }
  }
}
```

---

## Casos de Uso

### Apresentações

Remover pausas entre slides:

```bash
python -m src.cli.commands process apresentacao.mp4 \
  --remove-silence \
  --silence-db -45 \
  --silence-duration 1.0
```

### Entrevistas

Remover pausas para respirar:

```bash
python -m src.cli.commands process entrevista.mp4 \
  --remove-silence \
  --silence-db -40 \
  --silence-duration 0.5
```

### Tutorials

Remover momentos de reflexão:

```bash
python -m src.cli.commands process tutorial.mp4 \
  --remove-silence \
  --silence-db -50 \
  --silence-duration 0.8
```

---

## Limitações

A remoção de silêncio pode não funcionar bem em:

| Cenário | Problema | Solução |
|---------|---------|--------|
| Música de fundo | Considerada áudio | Ajuste threshold |
| Ruído ambiente | Falso positivo | Use detecção de audio mais alta |
| Áudio inconsistente | Corte incorreto | Ajuste duração mínima |
| Vídeo sem áudio | Não funciona | Use só detecção de cena |

---

## Combinando Com Detecção de Cenas

Para melhores resultados, combine detecção de cena com remoção de silêncio:

```bash
python -m src.cli.commands process video.mp4 \
  --visual-cut \
  --remove-silence
```

O sistema:
1. Primeiro detecta as mudanças de cena
2. Depois remove o silêncio dentro de cada clip

---

## Formato de Output

O relatório inclui informações sobre o silêncio removido:

```json
{
  "clips_detected": 5,
  "silence_removed": {
    "total_duration_removed": 12.5,
    "segments_removed": 8,
    "db_threshold": -40,
    "min_duration": 0.5
  }
}
```

---

## Dicas e Truques

### 1. Use Preview Primeiro

```bash
python -m src.cli.commands preview video.mp4
```

### 2. Ajuste o Threshold

Se remover demais, aumente o threshold:

```bash
python -m src.cli.commands process video.mp4 \
  --remove-silence \
  --silence-db -30
```

Se não remover o suficiente:

```bash
python -m src.cli.commands process video.mp4 \
  --remove-silence \
  --silence-db -50
```

### 3. Ajuste a Duração

Para vídeos com muitas pausas curtas:

```bash
python -m src.cli.commands process video.mp4 \
  --remove-silence \
  --silence-duration 0.3
```

Para vídeos com pausas longas:

```bash
python -m src.cli.commands process video.mp4 \
  --remove-silence \
  --silence-duration 2.0
```

---

## Próximos Passos

- **[Legendas](subtitles.md)** - Adicione legendas automáticas
- **[Processamento em Lote](batch-processing.md)** - Processe vários vídeos
- **[Exemplos Práticos](../examples/index.md)** - Mais casos

---

## Suporte

Para problemas, veja **[Solução de Problemas](../troubleshooting.md)**.

---

*Última atualização: 2026-04-29*