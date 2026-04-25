# Projeto: Automação de Cortes em Vídeos

## Visão Geral

Este documento contém todas as perguntas necessárias para definir o escopo e requisitos do projeto de automação de cortes em vídeos. Responda cada seção para que eu possa gerar a documentação adequada.

---

## 1. Escopo do Projeto

| #   | Pergunta                                      | Sua Resposta |
| --- | --------------------------------------------- | -------------|
| 1.1 | O que esses "cortes" devem fazer? Recortar trechos específicos, dividir em partes menores, ou remover seções? | eu quero que o programa avalie as partes que muda de cena para ter uma corte, ou se eu disser que quero remover os silencios tbm ele deve remover |
| 1.2 | Qual o objetivo principal? Produzir clips curtos para redes sociais, remover silêncio, criar highlight reels? | eu quero cortar eles para ajudar em edições para redes socias com youtube e instagram, até mesmo o tiktok|
| 1.3 | O projeto é para uso pessoal ou comercial? | para uso pessoal, mas se houver a possibilidade de ser algo que eu consiga colocar num pen-driver e usar em outra maquina eu gostaria  |

---

## 2. Origem e Formato dos Vídeos

| #   | Pergunta                                      | Sua Resposta |
| --- | --------------------------------------------- | -------------|
| 2.1 | De onde vêm os vídeos de entrada? Arquivos locais, pasta específica, URL, download automático? | serão arquivos locais, as pasta pode ser variadas por que tem diferentes videos |
| 2.2 | Quais formatos de vídeo são necessários suportar? (MP4, AVI, MKV, WebM, MOV?) | esses diferentes formatos seriam interressante mais mkv, avi e mp43 são prioridades |
| 2.3 | Qual resolução típica dos vídeos de entrada? (1080p, 4K, variados?) | variadas resoluções |
| 2.4 | Os vídeos já existem ouo sistema deve baixa-los de algum lugar? | os videos ja existem |

---

## 3. Definição de "Corte"

| #   | Pergunta                                      | Sua Resposta |
| --- | --------------------------------------------- | -------------|
| 3.1 | Como os trechos para cortar serão especificados? Por timestamps (início/fim), por arquivo de configuração, por planilha, detectados automaticamente? | O corte vai ser algo mais automatico, mas poderia ter um arquivo json com os pontos de corte|
| 3.2 | O sistema deve detectar os cortes automaticamente? Se sim, com base em que? (silêncio em áudio, silêncio visual/movimento, cenas específicas?) | sim, com base nas diferenças visuais e se quiser as partes de silencio também |
| 3.3 | Se for detecção automática, qual a sensibilidade desejada? (muito precisas,中等, folgadas?) | ela pode ser setada a sensibilidade, mais por padrão eu espero um meio termo |
| 3.4 | Os cuttings devem serpor remoção (cortar e colar) ou por extração (salvar só os trechos)? | pode salvar os trechos |

---

## 4. Processamento de Áudio

| #   | Pergunta                                      | Sua Resposta |
| --- | --------------------------------------------- | -------------|
| 4.1 | O sistema deve processar o áudio do vídeo? (detectar silêncio, normalizar volume, remover áudio) | sim deve mais gostaria que desse a opção se eu quero realizar esses tratamentos, mas seria bom ter esses tipos de tratamento|
| 4.2 | Se detectar silêncio em áudio: qual threshold? (-40dB, -50dB, outro?) | acredito que esse ponto pode varia |
| 4.3 | O silence detection já existe parcialmente no código (análise visual). Deve expandir para áudio real ou manter só visual? | expandir  |
| 4.4 | Os clips cortados devem manter o áudio original? | sim devem manter |

---

## 5. Formato de Saída

| #   | Pergunta                                      | Sua Resposta |
| --- | --------------------------------------------- | -------------|
| 5.1 | Qual formato de saída desejado? (MP4, WebM, mesmo do input?) | mesmo formato do input de preferencia |
| 5.2 | Qual codec de saída? (H.264, H.265, same do input?) | O mesmo di input |
| 5.3 | Qual bitrate ou resolução de saída? (mesmo do original, downscaling, específico?) | a mesma do original |
| 5.4 | Onde os vídeos cortados devem ser salvos? (pasta específica, mesmo diretório, conforme config?) | dever ser salvos no mesmo lugar da onde o video veio mas com uma pasta chamada clips |

---

## 6. Interface do Usuário

| #   | Pergunta                                      | Sua Resposta |
| --- | --------------------------------------------- | -------------|
| 6.1 | O sistema precisa de interface gráfica (GUI) ou só linha de comando (CLI)? |  seria bom uma interface |
| 6.2 | Se CLI, quais opções devem estar disponíveis? (listar no campo resposta) | remoção de silencio, aplicação de normalização no audio, deletar original no final do processo, adicionar legenda automatica no video, criar uma arquivo de legenda automatica, definir o quantidade de bd que pode ser considerada silencio, e um trashhold de tempo que tem que ter entre os cortes de silencio, um trhreshold para os cortes de video, uma flag para dizer que o video não tem audio |
| 6.3 | O sistema deve gerarLog/relatório do processamento? (JSON, CSV, texto?) | JSON |
| 6.4 | Deseja visualizar preview antes de processar? | se possivel sim |

---

## 7. Estrutura do Projeto

| #   | Pergunta                                      | Sua Resposta |
| --- | --------------------------------------------- | -------------|
| 7.1 | O código existente deve ser expandido ou reescrito? | pode ser rescrito, expandido não mas se der pra reaproveitar okau |
| 7.2 | Há necessidade de arquivo de configuração (YAML/JSON)? | pode ser JSON |
| 7.3 | O projeto deve ter estrutura de package (módulos separados)? | sim sempre  |
| 7.4 | Deseja criar testes unitários? | Sim sempre  |

---

## 8. Integrações e Dependências

| #   | Pergunta                                      | Sua Resposta |
| --- | --------------------------------------------- | -------------|
| 8.1 | FFmpeg está instalado no ambiente? |  não |
| 8.2 | Outras bibliotecas necessárias? (pydub para áudio, moviepy, scenedetect já incluso?) | não |
| 8.3 | O sistema deve se integrar com algo externo? (Cloud storage, Discord, Telegram?) | não |

---

## 9. Critérios de Qualidade

| #   | Pergunta                                      | Sua Resposta |
| --- | --------------------------------------------- | -------------|
| 9.1 | Quais critérios de qualidade de saída? (mesma qualidade, otimizado para web, tradeoff tamanho/qualidade?) |  nesna qualidade de entrada na saida |
| 9.2 | O sistema deve validar o vídeo de saída? (reproduzir, verificar integridade?) | |
| 9.3 | Qual tolerância para erros? (parar tudo, continuar com warning, pular arquivo?) | |
| 9.4 | Há necessidade de backup dos originais antes de processar? | os originais não devem ser alterados a menos que exista uma flag de destroi como ativa, caso a flag não esteja ele so cria novos arquivos |

---

## 10. Futures (Opcional)

| #   | Pergunta                                      | Sua Resposta |
| --- | --------------------------------------------- | -------------|
| 10.1 |需求 adicional no futuro? (detecção de faces, transcrição, legendasautomáticas?) | pode ter uma opção de adicionar a legenda no video ou gerar uma arquivo com a legenda criar para depois em programas como premier e capcut colocar nos videos  |
| 10.2 |Escala de uso: poucos vídeos por vez ou processamento em lote (batch)? | um video por vez ou processamento batch  |
| 10.3 |Precisa de paralelização (múltiplos vídeos simultâneos)? | gostaria de sim |

---

## Próximos Passos

Após responder este formulário, poderemos:

1. Gerar **Requirements Report** com os requisitos documentados
2. Criar **Acceptance Criteria** para cada feature
3. Planejar a **Arquitetura da Solução**
4. Corrigir e expandir o código existente

---

*Documento gerado em: 2026-04-24*