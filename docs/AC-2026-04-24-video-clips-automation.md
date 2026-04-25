# Acceptance Criteria - Video Clips Automation

| Metadata           | Valor                                              |
| ------------------ | -------------------------------------------------- |
| **Documento**      | AC-2026-04-24-video-clips-automation.md            |
| **Versão**         | 1.0                                                |
| **Data**           | 2026-04-24                                         |
| **Autor**          | PO Agent                                           |
| **Status**         | Draft                                              |
| **Skill**          | acceptance-criteria-generator                      |
| **Parent Doc**     | REQ-2026-04-24-video-clips-automation.md           |

---

## 1. Core Features - Detecção e Corte

### 1.1 Detecção Visual de Cena

| ID      | Tipo      | Critério | Critério de Teste | Prioridade |
| ------- | --------- | -------- | ------------------ | ---------- |
| AC-101  | Happy     | Sistema detecta mudanças de cena via análise de frames | Frame diff > threshold = novo corte | Must |
| AC-102  | Happy     | Sensibilidade configurável (baixa, média, alta) | Threshold 0.3x, 1.0x, 2.0x | Must |
| AC-103  | Borda     | Vídeo sem mudança de cena gera 0 clips | Output pasta vazia, report com count=0 | Should |
| AC-104  | Erro      | Vídeo corrompido retorna erro legível | "Video file corrupted" + exit code 1 | Must |

### 1.2 Remoção de Silêncio

| ID      | Tipo      | Critério | Critério de Teste | Prioridade |
| ------- | --------- | -------- | ------------------ | ---------- |
| AC-201  | Happy     | Detecta silêncio em áudio com threshold em dB | Silêncio < -40dB (padrão) = detectado | Must |
| AC-202  | Happy     | Threshold configurável pelo usuário | CLI --silence-db e --silence-duration | Must |
| AC-203  | Happy     | Remove trechos silenciosos do vídeo | output.mp4 sem silêncio entre timestamps | Must |
| AC-204  | Happy     | Preserva áudio não-silencioso | dB > threshold mantém áudio | Must |
| AC-205  | Borda     | Vídeo sem áudio é processado corretamente | Flag --no-audio evita erro | Must |
| AC-206  | Erro      | FFmpeg não encontrado retorna erro | "FFmpeg required but not found" | Must |

---

## 2. Interface de Usuário

### 2.1 CLI (Command Line Interface)

| ID      | Tipo      | Critério | Critério de Teste | Prioridade |
| ------- | --------- | -------- | ------------------ | ---------- |
| AC-301  | Happy     | CLI aceita path de vídeo como argumento | `clip-tool video.mp4` funciona | Must |
| AC-302  | Happy     | CLI aceita --remove-silence flag | Flag habilita detecção de silêncio | Must |
| AC-303  | Happy     | CLI aceita --visual-cut flag | Flag habilita corte por cena | Must |
| AC-304  | Happy     | CLI aceita --normalize-audio flag | Flag normaliza volume | Should |
| AC-305  | Happy     | CLI aceita --destroy flag | Flag deleta original após processar | Should |
| AC-306  | Happy     | CLI aceita --generate-subtitles flag | Flag gera legendas via Whisper | Should |
| AC-307  | Happy     | CLI aceita --export-subtitles flag | Flag exporta SRT/VTT | Should |
| AC-308  | Happy     | CLI aceita --no-audio flag | Flag indica vídeo sem áudio | Should |
| AC-309  | Happy     | CLI aceita --config path | Carrega config de arquivo JSON | Should |
| AC-310  | Happy     | CLI aceita --batch path | Processa múltiplos vídeos | Must |
| AC-311  | Erro      | Argumentos inválidos retornam help | `clip-tool --invalid` mostra help | Must |

### 2.2 GUI (Graphical User Interface)

| ID      | Tipo      | Critério | Critério de Teste | Prioridade |
| ------- | --------- | -------- | ------------------ | ---------- |
| AC-401  | Happy     | GUI exibe preview de vídeo | Mini-player carrega e toca | Should |
| AC-402  | Happy     | GUI exibe timeline com pontos de corte | Markers visíveis na timeline | Must |
| AC-403  | Happy     | GUI permite ajuste manual de cortes | Drag markers ajusta timestamps | Should |
| AC-404  | Happy     | GUI exibe frames dos pontos de corte | Thumbnails nos markers | Should |
| AC-405  | Happy     | GUI permite iniciar processamento | Botão "Processar" executa pipeline | Must |
| AC-406  | Happy     | GUI exibe progresso do processamento | Progress bar atualiza em tempo real | Should |

---

## 3. Processamento e Output

### 3.1 Pipeline de Processamento

| ID      | Tipo      | Critério | Critério de Teste | Prioridade |
| ------- | --------- | -------- | ------------------ | ---------- |
| AC-501  | Happy     | Processa vídeo mantendo codec original | Codec input = codec output | Must |
| AC-502  | Happy     | Processa vídeo mantendo bitrate original | Bitrate input = bitrate output | Must |
| AC-503  | Happy     | Processa vídeo mantendo resolução original | WxH input = WxH output | Must |
| AC-504  | Happy     | Salva clips em pasta `clips/` | `video.mp4/clips/clip_001.mp4` | Must |
| AC-505  | Happy     | Não modifica arquivo original | `video.mp4` inalterado após processar | Must |
| AC-506  | Happy     | Com --destroy flag, deleta original | Original removido após sucesso | Should |
| AC-507  | Happy     | Gera report.json na pasta de saída | JSON com metadata e clips | Must |
| AC-508  | Happy     | Processamento em batch paralleliza | 3 vídeos processam simultaneamente | Should |

### 3.2 Formatos Suportados

| ID      | Tipo      | Critério | Critério de Teste | Prioridade |
| ------- | --------- | -------- | ------------------ | ---------- |
| AC-601  | Happy     | Aceita MP4 como input | Processa .mp4 corretamente | Must |
| AC-602  | Happy     | Aceita MKV como input | Processa .mkv corretamente | Must |
| AC-603  | Happy     | Aceita AVI como input | Processa .avi corretamente | Must |
| AC-604  | Happy     | Aceita WebM como input | Processa .webm corretamente | Should |
| AC-605  | Happy     | Aceita MOV como input | Processa .mov corretamente | Should |

---

## 4. Legendas

### 4.1 Geração de Legendas

| ID      | Tipo      | Critério | Critério de Teste | Prioridade |
| ------- | --------- | -------- | ------------------ | ---------- |
| AC-701  | Happy     | Whisper local transcreve áudio | Texto gerado corresponde ao áudio | Must |
| AC-702  | Happy     | Gera arquivo SRT com timestamps | SRT com index, timecode, texto | Must |
| AC-703  | Happy     | Gera arquivo VTT com timestamps | VTT com timecode, texto | Should |
| AC-704  | Happy     | Insere legendas no vídeo se --burn-subtitles | Legendas visíveis no vídeo output | Should |
| AC-705  | Erro      | Falha no Whisper retorna erro | "Subtitle generation failed" + detalhes | Must |

---

## 5. Relatórios

### 5.1 Relatório JSON

| ID      | Tipo      | Critério | Critério de Teste | Prioridade |
| ------- | --------- | -------- | ------------------ | ---------- |
| AC-801  | Happy     | Report contém input_video path | `report.json.input_video` = arquivo | Must |
| AC-802  | Happy     | Report contém processing_date | ISO 8601 format | Must |
| AC-803  | Happy     | Report contém options aplicadas | `report.json.options` com flags | Must |
| AC-804  | Happy     | Report contém clips[] array | Cada clip com id, start, end, reason | Must |
| AC-805  | Happy     | Report contém clips_detected count | `report.json.clips_detected` = int | Must |

---

## 6. Definição de Pronto (Definition of Done)

### Funcional
- [ ] Todos os ACs Must com status "passing"
- [ ] CLI funcional com todas as flags documentadas
- [ ] GUI funcional com preview e timeline
- [ ] Legendas funcionando com Whisper local
- [ ] Report JSON gerado corretamente

### Não-Funcional
- [ ] Testes unitários cobrindo funcionalidades core
- [ ] Código modular com packages separados
- [ ] Documentação de uso (README + CLI help)
- [ ] Portável (executável em USB)

---

## 7. Matriz de Prioridades

| Prioridade | Definição              | ACs                        |
| ---------- | ---------------------- | -------------------------- |
| Must       | Essencial para MVP     | AC-101, AC-102, AC-201-AC-206, AC-301-AC-310, AC-501-AC-507, AC-601-AC-605, AC-701-AC-705, AC-801-AC-805 |
| Should     | Importante             | AC-103, AC-303-AC-308, AC-401-AC-406, AC-601-AC-604, AC-702, AC-704 |
| Could      | Desejável             | AC-104, AC-311, AC-505, AC-508 |

---

*Documento gerado pelo PO Agent - Skills: acceptance-criteria-generator*