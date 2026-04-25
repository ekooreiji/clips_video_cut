# BDD Scenarios - Video Clips Automation

| Metadata           | Valor                                    |
| ------------------ | ---------------------------------------- |
| **Documento**      | BDD-2026-04-24-video-clips-automation.md |
| **Versão**         | 1.0                                      |
| **Data**           | 2026-04-24                               |
| **Autor**          | PO Agent                                 |
| **Status**         | Draft                                    |
| **Skill**          | bdd-scenarios                            |
| **Parent Doc**     | REQ-2026-04-24-video-clips-automation.md |

---

## Feature: Detecção Visual de Cena

**Descrição:** Sistema deve detectar automaticamente mudanças de cena em vídeos através de análise de frames, permitindo cortes precisos nos pontos de transição.

### Scenario: Detectar mudança de cena com threshold padrão
```
Given que o usuário executa o comando com um vídeo válido
And a sensibilidade padrão está configurada (média)
When o sistema analisa os frames do vídeo
Then o sistema deve identificar pontos de mudança de cena
And salvar cada trecho como um clip separado
```

### Scenario: Detectar mudança de cena com sensibilidade alta
```
Given que o usuário executa o comando com --sensitivity high
When o sistema analisa os frames com threshold 2.0x
Then o sistema deve identificar apenas mudanças drásticas de cena
And gerar menos clips que o padrão
```

### Scenario: Detectar mudança de cena com sensibilidade baixa
```
Given que o usuário executa o comando com --sensitivity low
When o sistema analisa os frames com threshold 0.3x
Then o sistema deve identificar qualquer variação mínima
And gerar mais clips que o padrão
```

### Scenario: Vídeo sem mudança de cena
```
Given que o usuário executa o comando com um vídeo estático
When o sistema analisa os frames
Then o sistema deve criar relatório com clips_detected = 0
And não criar arquivos de clip
```

### Scenario: Vídeo corrompido
```
Given que o usuário executa o comando com um vídeo corrompido
When o sistema tenta abrir o arquivo
Then o sistema deve retornar erro legível
And exit code deve ser 1
```

---

## Feature: Remoção de Silêncio em Áudio

**Descrição:** Sistema deve detectar e remover trechos de silêncio do áudio de um vídeo baseado em threshold configurável de dB.

### Scenario: Remover silêncio com threshold padrão
```
Given que o usuário executa o comando com --remove-silence
And o threshold de silêncio padrão é -40dB
When o sistema detecta trechos com áudio abaixo de -40dB
Then o sistema deve remover esses trechos
And concatenar os trechos com áudio
And gerar vídeo sem silêncio
```

### Scenario: Remover silêncio com threshold customizado
```
Given que o usuário executa o comando com --remove-silence --silence-db -50
When o sistema detecta trechos com áudio abaixo de -50dB
Then o sistema deve usar o threshold customizado
And remover silêncio baseado no novo threshold
```

### Scenario: Remover silêncio com duração mínima
```
Given que o usuário executa o comando com --remove-silence --silence-duration 1.0
When o sistema detecta silêncio
Then o sistema deve apenas remover silêncio com duração >= 1.0 segundo
And ignorar silêncio menor
```

### Scenario: Vídeo sem áudio
```
Given que o usuário executa o comando com --remove-silence em vídeo sem áudio
When o sistema verifica presença de áudio
Then o sistema deve informar que não há áudio para processar
And continuar o processamento sem erro
```

### Scenario: Vídeo sem silêncio
```
Given que o usuário executa o comando com --remove-silence
And o vídeo não contém trechos silenciosos
When o sistema analisa o áudio
Then o sistema deve manter o vídeo inalterado
And reportar que não houve silêncio detectado
```

---

## Feature: Processamento em Lote (Batch)

**Descrição:** Sistema deve processar múltiplos vídeos simultaneamente com suporte a paralelização.

### Scenario: Processar múltiplos vídeos em paralelo
```
Given que o usuário executa o comando com --batch /pasta/videos
When a pasta contém 5 vídeos
Then o sistema deve processar até 3 vídeos simultaneamente
And continuar até todos processados
```

### Scenario: Batch com arquivo de configuração
```
Given que o usuário executa o comando com --batch e --config config.json
When o sistema inicia o processamento
Then o sistema deve aplicar as configurações do JSON
And aplicar em todos os vídeos do batch
```

### Scenario: Batch com erro em um vídeo
```
Given que o usuário executa o comando com --batch /pasta/videos
And a pasta contém um vídeo válido e um corrompido
When o sistema processa os vídeos
Then o sistema deve continuar com o vídeo válido
And registrar erro do vídeo corrompido no report
And não abortar processamento dos demais
```

---

## Feature: Interface CLI

**Descrição:** Interface de linha de comando deve permitir configuração completa do processamento via flags.

### Scenario: CLI com argumento obrigatório
```
Given que o usuário executa o comando sem argumento de vídeo
When o sistema processa a entrada
Then o sistema deve exibir mensagem de erro
And mostrar help comUsage correto
```

### Scenario: CLI com flags de processamento
```
Given que o usuário executa o comando "clip-tool video.mp4 --remove-silence --visual-cut"
When o sistema processa
Then o sistema deve aplicar ambos os processamentos
And gerar clips dos cortes visuais E áudio processado
```

### Scenario: CLI com flag --destroy
```
Given que o usuário executa o comando com --destroy
When o processamento completa com sucesso
Then o sistema deve excluir o arquivo original
And manter apenas os clips gerados
```

### Scenario: CLI com arquivo de configuração
```
Given que o usuário executa o comando com --config settings.json
When o sistema carrega o arquivo
Then o sistema deve aplicar todas as opções do JSON
And sobrescrever valores padrão
```

---

## Feature: Interface GUI

**Descrição:** Interface gráfica deve permitir visualização, ajuste e execução do processamento.

### Scenario: GUI exibe preview do vídeo
```
Given que o usuário abre o GUI com um vídeo carregado
When o vídeo é selecionado
Then o sistema deve exibir mini-player com controles básicos
And permitir play/pause do vídeo
```

### Scenario: GUI exibe timeline com marcadores de corte
```
Given que o usuário abre o GUI com um vídeo carregado
When o sistema detecta pontos de corte
Then o sistema deve exibir marcadores na timeline
And cada marcador deve ser clicável para ajuste
```

### Scenario: GUI permite ajuste manual de cortes
```
Given que o usuário visualiza a timeline com marcadores
When ele arrasta um marcador para nova posição
Then o sistema deve atualizar o timestamp do corte
And recalcular preview se disponível
```

### Scenario: GUI exibe progresso do processamento
```
Given que o usuário clica em "Processar"
When o processamento inicia
Then o sistema deve exibir barra de progresso
And atualizar em tempo real
And mostrar logs de cada etapa
```

---

## Feature: Geração de Legendas

**Descrição:** Sistema deve gerar legendas automáticas usando Whisper local e exportar em formatos SRT/VTT.

### Scenario: Gerar legendas com Whisper local
```
Given que o usuário executa o comando com --generate-subtitles
And o vídeo contém áudio
When o sistema processa com Whisper local
Then o sistema deve transcrever o áudio
And gerar timestamps para cada frase
```

### Scenario: Exportar legendas em SRT
```
Given que o usuário executa o comando com --export-subtitles --format srt
When o processamento completa
Then o sistema deve gerar arquivo .srt na pasta de saída
And o arquivo deve conter index, timecode e texto
```

### Scenario: Exportar legendas em VTT
```
Given que o usuário executa o comando com --export-subtitles --format vtt
When o processamento completa
Then o sistema deve gerar arquivo .vtt na pasta de saída
And o arquivo deve seguir o formato WebVTT
```

### Scenario: Queimar legendas no vídeo
```
Given que o usuário executa o comando com --burn-subtitles
When o processamento completa
Then o sistema deve inserir legendas no vídeo
And o vídeo output deve conter legendas visíveis
```

---

## Feature: Output e Relatórios

**Descrição:** Sistema deve manter qualidade original e gerar relatórios estruturados em JSON.

### Scenario: Manter codec original
```
Given que o usuário executa o comando com um vídeo H.264
When o processamento completa
Then o vídeo output deve usar codec H.264
And não converter para outro codec
```

### Scenario: Manter resolução original
```
Given que o usuário executa o comando com um vídeo 1920x1080
When o processamento completa
Then o vídeo output deve ter resolução 1920x1080
And não redimensionar
```

### Scenario: Salvar na pasta clips
```
Given que o usuário executa o comando com video.mp4
When o processamento completa
Then o sistema deve criar pasta video.mp4/clips/
And salvar os clips dentro dessa pasta
```

### Scenario: Gerar report.json
```
Given que o usuário executa o comando com um vídeo
When o processamento completa
Then o sistema deve criar report.json na pasta clips/
And o report deve conter input_video, processing_date, options, clips_detected, clips[]
```

### Scenario: Não modificar original sem --destroy
```
Given que o usuário executa o comando SEM --destroy
When o processamento completa
Then o sistema deve manter video.mp4 inalterado
And apenas criar novos arquivos
```

---

## Feature: Configuração via JSON

**Descrição:** Sistema deve permitir configuração completa via arquivo JSON.

### Scenario: Carregar configuração completa
```
Given que o usuário cria config.json com todas as opções
When o sistema carrega com --config config.json
Then o sistema deve aplicar todas as configurações
And ignorar valores padrão
```

### Scenario: Configuração com valores inválidos
```
Given que o usuário cria config.json com valores inválidos
When o sistema tenta carregar
Then o sistema deve reportar erro de validação
And indicando qual campo está inválido
```

---

## Feature: Paralelização

**Descrição:** Sistema deve processar múltiplos vídeos simultaneamente usando multiprocessing e threading.

### Scenario: Paralelização com multiprocessing (CPU-bound)
```
Given que o usuário executa o comando com --batch /pasta
And o processamento inclui detecção visual (CPU-intensive)
When o sistema inicia processamento
Then o sistema deve usar multiprocessing para paralelização
And utilizar múltiplos cores de CPU
```

### Scenario: Paralelização com threading (I/O-bound)
```
Given que o usuário executa o comando com --batch /pasta
And o processamento inclui escrita de arquivos (I/O-intensive)
When o sistema inicia processamento
Then o sistema deve usar threading para operações de I/O
And maximizar throughput de disco
```

---

*Documento gerado pelo PO Agent - Skills: bdd-scenarios*