# Video Clips Automation

Bem-vindo à documentação do **Video Clips Automation**, uma ferramenta poderosa para criadores de conteúdo que desejam gerar clips para redes sociais de forma automática.

## O que é o Video Clips Automation?

O Video Clips Automation é um sistema que ajuda você a:
- **Detectar automaticamente mudanças de cena** nos vídeos
- **Remover trechos de silêncio** indesejados
- **Gerar legendas automáticas** usando inteligência artificial
- **Normalizar o volume** do áudio
- **Processar múltiplos vídeos** em lote

## Por que usar esta ferramenta?

| Benefício | Descrição |
|-----------|-----------|
| Economia de tempo | Corte manual leva horas, a ferramenta faz em minutos |
| Consistência | Critérios uniformes para todos os clips |
| Automação | Processe hundreds de vídeos de uma vez |
| Legendas AI | Gere legendas automaticamente com Whisper |

## Principais Funcionalidades

### 1. Detecção de Cenas
Identifica automaticamente onde uma cena termina e outra começa no vídeo. Perfeito para:
- Vídeos de tutorial
- Gameplays
- Vlogs
- Entrevistas

### 2. Remoção de Silêncio
Remove automaticamente partes do vídeo onde não há áudio relevante:
- Pausas para respirar
- Momentos de reflexão
- Intervalos entre falas

### 3. Legendas Automáticas
Gera legendas usando IA (Whisper):
- Formatos SRT e VTT
- Queima legendas no vídeo
- Múltiplos modelos de IA

### 4. Processamento em Lote
Processa todos os vídeos de uma pasta:
- Suporta múltiplos formatos
-parallel processing
- Relatório de resultados

## Guia Rápido

### Processando seu primeiro vídeo

```bash
# Instalação
pip install -r requirements.txt

# Processar vídeo com detecção de cenas
python -m src.cli.commands process meuvideo.mp4

# Ver preview antes de processar
python -m src.cli.commands preview meuvideo.mp4
```

### Resultado típico

```
Video: meuvideo.mp4
Clips detectados: 8
Arquivo de relatório: meuvideo.mp4/clips/report.json
```

## Formatos Suportados

| Formato | Extensão | Suportado |
|--------|----------|-----------|
| MP4 | .mp4 | ✓ |
| Matroska | .mkv | ✓ |
| AVI | .avi | ✓ |
| WebM | .webm | ✓ |
| QuickTime | .mov | ✓ |

## Próximos Passos

Pronto para começar? Siga estes guias:

1. **[Instalação](setup/installation.md)** - Configure o ambiente
2. **[Guia Rápido](setup/quick-start.md)** - Primeiro processamento
3. **[Interface CLI](user-guide/cli.md)** - Comandos disponíveis
4. **[Exemplos Práticos](examples/index.md)** - Use casos comuns

## Suporte

Encontrou algum problema? Consulte:
- **[Solução de Problemas](troubleshooting.md)** - Problemas comuns
- **GitHub Issues** - Reportar bugs

---

*Video Clips Automation v1.0.0* - documentation generated with MkDocs Material