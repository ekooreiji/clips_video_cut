# Requirements Report - Automação de Cortes em Vídeos

| Metadata           | Valor                                    |
| ------------------ | ---------------------------------------- |
| **Documento**      | REQ-2026-04-24-video-clips-automation.md |
| **Versão**         | 1.0                                      |
| **Data**           | 2026-04-24                               |
| **Autor**          | PO Agent                                 |
| **Status**         | Em Análise                               |
| **Skill**          | requirements-analyzer                    |

---

## 1. Visão Geral do Projeto

**Nome:** Video Clips Automation

**Resumo:** Sistema CLI/GUI para automatizar cortes de vídeos baseado em detecção de mudança de cena e remoção de silêncio em áudio, com suporte a legendas automáticas via Whisper local.

**Público-Alvo:** Criadores de conteúdo para YouTube, Instagram, TikTok (uso pessoal).

---

## 2. Requisitos Funcionais

| ID   | Tipo        | Descrição                                                                 |
| ---- | ----------- | ------------------------------------------------------------------------- |
| RF-01 | Funcional   | Detectar mudanças de cena automaticamente via análise visual de frames    |
| RF-02 | Funcional   | Detectar silêncio em áudio com threshold configurável                    |
| RF-03 | Funcional   | Remover seções de silêncio do áudio quando habilitado                     |
| RF-04 | Funcional   | Cortar/extrair trechos de vídeo em novos arquivos                         |
| RF-05 | Funcional   | Processar arquivos locais (MP4, MKV, AVI, WebM, MOV)                       |
| RF-06 | Funcional   | Interface CLI com opções configuráveis                                     |
| RF-07 | Funcional   | Interface GUI para visualização e execução                                |
| RF-08 | Funcional   | Gerar relatório de processamento em formato JSON                          |
| RF-09 | Funcional   | Manter qualidade original do vídeo (mesmo codec, bitrate, resolução)       |
| RF-10 | Funcional   | Salvar clips na pasta `clips/` junto ao vídeo original                    |
| RF-11 | Funcional   | Permitir arquivo JSON com timestamps de corte customizados                |
| RF-12 | Funcional   | Opção para normalizar volume do áudio                                     |
| RF-13 | Funcional   | Opção para adicionar legendas automáticas (Whisper local)                 |
| RF-14 | Funcional   | Opção para exportar legendas em arquivo (SRT/VTT)                         |
| RF-15 | Funcional   | Opção para excluir arquivo original após processamento                     |
| RF-16 | Funcional   | Flag para indicar que o vídeo não tem áudio                               |
| RF-17 | Funcional   | Configurar threshold de sensibilidade para cortes visuais                  |
| RF-18 | Funcional   | Configurar threshold de tempo mínimo entre cortes de silêncio            |
| RF-19 | Funcional   | Configurar threshold de dB para detecção de silêncio em áudio             |
| RF-20 | Funcional   | Preview dos pontos de corte antes de processar                           |
| RF-21 | Funcional   | Processamento em lote (batch) de múltiplos vídeos                         |
| RF-22 | Funcional   | Paralelização para múltiplos vídeos simultâneos                            |

---

## 3. Requisitos Não-Funcionais

| ID    | Tipo             | Descrição                                                      |
| ----- | ---------------- | -------------------------------------------------------------- |
| RNF-01 | Performance     | Processamento em paralelo (multiprocessing + threading)         |
| RNF-02 | Portabilidade   | Executável portable (USB) para uso em outras máquinas          |
| RNF-03 | Robustez        | Não modificar arquivos originais (backup apenas se flag ativa) |
| RNF-04 | Usabilidade     | CLI intuitiva e GUI acessível                                   |
| RNF-05 | Compatibilidade | Suporte a Windows                                               |
| RNF-06 | Manutenibilidade| Arquitetura modular com packages separados                     |
| RNF-07 | Qualidade       | Testes unitários para todas as funcionalidades principais      |

---

## 4. Casos de Uso

### UC-01: Corte Automático por Cena
```
Título: Corte Automático por Cena
Ator: Criador de Conteúdo
Pré-condição: Vídeo existente no sistema
Fluxo Principal:
  1. Usuário executa CLI ou GUI
  2. Sistema analisa frames do vídeo
  3. Sistema detecta mudanças de cena
  4. Sistema exibe preview dos cortes
  5. Usuário confirma ou ajusta
  6. Sistema corta o vídeo
  7. Sistema salva na pasta clips/
Pós-condição: Clips gerados na pasta de saída
```

### UC-02: Remoção de Silêncio
```
Título: Remoção de Silêncio em Áudio
Ator: Criador de Conteúdo
Pré-condição: Vídeo com áudio
Fluxo Principal:
  1. Usuário habilita flag --remove-silence
  2. Usuário configura threshold (dB, tempo mínimo)
  3. Sistema detecta silêncio no áudio
  4. Sistema remove trechos silenciosos
  5. Sistema salva vídeo processado
Pós-condição: Vídeo sem silêncio
```

### UC-03: Legendas Automáticas
```
Título: Gerar Legendas Automáticas
Ator: Criador de Conteúdo
Pré-condição: Vídeo com áudio
Fluxo Principal:
  1. Usuário habilita flag --generate-subtitles
  2. Sistema extrai áudio do vídeo
  3. Sistema processa com Whisper local
  4. Sistema gera arquivo SRT/VTT
  5. Opcional: Insere legendas no vídeo
Pós-condição: Arquivo de legendas gerado
```

---

## 5. Regras de Negócio

| ID   | Regra                                                                 |
| ---- | --------------------------------------------------------------------- |
| RN-01 | Vídeos originais NÃO são modificados a menos que flag --destroy ativa  |
| RN-02 | Clips são salvos em `{diretorio_original}/clips/`                      |
| RN-03 | Sensibilidade padrão para detecção: média (threshold = 1.0x)          |
| RN-04 | Threshold de silêncio padrão: -40dB                                   |
| RN-05 | Tempo mínimo entre silêncio: 0.5 segundos                             |
| RN-06 | Codec de saída: mesmo do input                                       |

---

## 6. Dúvidas em Aberto

| #   | Pergunta                                                              | Status       |
| --- | --------------------------------------------------------------------- | ------------ |
| 1   | Qual tamanho máximo de vídeo para processamento?                      | **Sem limite** |
| 2   | Quantidade máxima de vídeos no batch?                                 | **10 simultâneos** |
| 3   | Qual formato preferido para relatório JSON? (schema específico?)      | **Schema definido** |

---

## 7. Formato de Saída Esperado

### 7.1 Estrutura de Pastas
```
diretorio_video/
├── video_original.mp4
└── clips/
    ├── video_original_clip_001.mp4
    ├── video_original_clip_002.mp4
    └── report.json
```

### 7.2 Relatório JSON
```json
{
  "input_video": "video_original.mp4",
  "processing_date": "2026-04-24T10:30:00",
  "options": {
    "remove_silence": true,
    "visual_cut": true,
    "normalize_audio": false
  },
  "clips_detected": 15,
  "clips": [
    {
      "id": 1,
      "start_time": 0.0,
      "end_time": 15.5,
      "reason": "scene_change"
    }
  ]
}
```

---

## 8. Próximos Passos

| #   | Ação                                    | Prioridade |
| --- | --------------------------------------- | ---------- |
| 1   | Confirmar ambiguidades acima            | Alta       |
| 2   | Gerar Acceptance Criteria                | Alta       |
| 3   | Criar BDD Scenarios                     | Média      |
| 4   | Planejar Arquitetura                     | Alta       |

---

*Documento gerado pelo PO Agent - Skills: requirements-analyzer*