# Solução de Problemas

Esta página lista os problemas mais comuns e suas soluções.

---

## Problemas de Instalação

### "python: command not found"

**Problema:** Python não está instalado ou não está no PATH.

**Solução:**

1. Verifique se o Python está instalado:
   ```bash
   python --version
   ```
   Se não estiver, instale-o.

2. No Windows, adicione ao PATH:
   - Abra "Sistema" > "Propriedades Avançadas"
   - Clique em "Variáveis de Ambiente"
   - Edite a variável "Path" e adicione o caminho do Python

### "ffmpeg: command not found"

**Problema:** FFmpeg não está instalado ou não está no PATH.

**Solução:**

1. Instale o FFmpeg (veja [Instalação](setup/installation.md))

2. No Windows, adicione ao PATH:
   ```powershell
   # Usando Chocolatey
   choco install ffmpeg
   ```

3. Verifique:
   ```bash
   ffmpeg -version
   ```

### "ModuleNotFoundError: No module named 'cv2'"

**Problema:** OpenCV não está instalado.

**Solução:**

```bash
pip install opencv-python
```

### "ModuleNotFoundError: No module named 'whisper'"

**Problema:** Whisper não está instalado.

**Solução:**

```bash
pip install whisper
```

---

## Problemas de Processamento

### "Nenhum clip detectado"

**Causas possíveis:**
1. Vídeo sem mudanças de cena
2. Sensibilidade muito alta
3. Threshold muito alto

**Soluções:**

1. **Ajuste a sensibilidade:**
   ```bash
   # Diminua a sensibilidade
   python -m src.cli.commands process video.mp4 --sensitivity low
   ```

2. **Reduza o sample_rate:**
   ```bash
   # Analisar mais quadros
   python -m src.cli.commands process video.mp4 --sample-rate 3
   ```

3. **Use detecção de silêncio:**
   ```bash
   python -m src.cli.commands process video.mp4 --remove-silence
   ```

### "Muitos clips detectados"

**Causa:** Sensibilidade muito alta.

**Solução:**

```bash
# Aumente a sensibilidade
python -m src.cli.commands process video.mp4 --sensitivity high
```

### "Silêncio não está sendo removido"

**Causas:**
1. Threshold muito alto (pouco sensível)
2. Duração mínima muito longa

**Solução:**

```bash
# Decrease threshold (mais sensível)
python -m src.cli.commands process video.mp4 \
  --remove-silence \
  --silence-db -50

# Diminua a duração mínima
python -m src.cli.commands process video.mp4 \
  --remove-silence \
  --silence-duration 0.3
```

### "Vídeo muito grande"

**Causa:** Arquivo ultrapassa 10GB.

**Solução:**

1. Divida o vídeo em partes menores
2. Comprimindo:
   ```bash
   ffmpeg -i video_original.mp4 -c:v libx264 -crf 23 video_comprimido.mp4
   ```

---

## Problemas de Áudio

### "Legendas não são geradas"

**Causas:**
1. Whisper não está instalado
2. Vídeo sem áudio
3. Áudio muito ruim

**Solução:**

1. Verifique se Whisper está instalado:
   ```bash
   pip install whisper
   ```

2. Especifique que o vídeo não tem áudio:
   ```bash
   python -m src.cli.commands process video.mp4 --no-audio
   ```

3. Use modelo mais leve:
   ```bash
   # Configuração
   {
     "subtitles": {
       "whisper_model": "tiny"
     }
   }
   ```

### "Transcrição imprecisa"

**Causa:** Modelo muito leve ou áudio ruído.

**Solução:**

1. Use modelo melhor:
   ```json
   {
     "subtitles": {
       "whisper_model": "small"
     }
   }
   ```

2. Limpe o áudio antes (avançado)

---

## Problemas de Saída

### "Clips salvos em pasta errada"

**Causa:** Diretório de saída não especificado corretamente.

**Solução:**

```bash
# Especifique o diretório
python -m src.cli.commands process video.mp4 -o ./minha_pasta
```

### "Arquivo original foi deletado"

**Causa:** Flag --destroy foi usada.

**Solução:**
- Não use --destroy se quiser manter o original
- Restoration só é possível do backup

---

## Problemas de Configuração

### "JSON inválido"

**Erro:** "Expecting property name enclosed in double quotes"

**Causa:** Aspas simples usadas em vez de aspas duplas.

**Solução:**
Use aspas duplas:

```json
// ERRADO
{ 'sensitivity': 1.0 }

// CORRETO
{ "sensitivity": 1.0 }
```

### "Configuração ignorada"

**Causa:** Opções CLI sobrescrevem config.

**Solução:**
- Use só o config:
  ```bash
  python -m src.cli.commands process video.mp4 -c config.json
  ```
- Ou use as opções com config:
  ```bash
  # Opções da CLI têm prioridade
  python -m src.cli.commands process video.mp4 -c config.json --sensitivity high
  ```

---

## Problemas de Interface Gráfica (GUI)

### "Erro: PyQt6 não está instalado"

**Solução:**

```bash
pip install PyQt6
```

### "GUI não abre"

**Causas:**
1. PyQt6 não instalado
2. Problema de display

**Solução:**

1. Instale PyQt6:
   ```bash
   pip install PyQt6
   ```

2. No Linux, instale dependências:
   ```bash
   sudo apt install libxcb-xinerama0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0 libxkbcommon-x11-0
   ```

---

## Mensagens de Erro

### "FFmpeg não encontrado"

| Significado | Solução |
|------------|--------|
| FFmpeg não instalado | Instale o FFmpeg |
| FFmpeg não no PATH | Adicione ao PATH |

### "Vídeo não encontrado"

| Significado | Solução |
|------------|--------|
| Arquivo não existe | Verifique o caminho |
| Arquivo com nome errado | Corrija o nome |

### "Formato não suportado"

| Significado | Solução |
|------------|--------|
| Extensão não suportada | Use MP4, MKV, AVI, WebM ou MOV |

### "Vídeo corrompido"

| Significado | Solução |
|------------|--------|
| Arquivo de vídeo inválido | Use outro vídeo |

### "Memória insuficiente"

| Significado | Solução |
|------------|--------|
| Vídeo muito grande | Use vídeos menores |

---

## Códigos de Erro

| Código | Significado |
|--------|-------------|
| 0 | Sucesso |
| 1 | Erro genérico |
| 2 | Erro de argumento |
| 3 | Arquivo não encontrado |
| 4 | Erro de FFmpeg |

---

## Como Obter Ajuda

### Ver Logs

Para ver logs detalhados:

```bash
python -m src.cli.commands process video.mp4 -v
```

Os logs são salvos em `app.log`.

### Reportar Bug

Ao reportar um bug, inclua:

1. Comando executado
2. Arquivo de configuração (se usado)
3. Saída do comando
4. Log (se disponível)
5. Sistema operacional
6. Versão do Python

---

## Verificação de Saúde

Para verificar se tudo está instalado corretamente:

```bash
python -c "
import cv2
import whisper
import ffmpeg
print('Todas as dependências OK!')
"
```

Se não houver erro, está tudo bem.

---

## Próximos Passos

Se o problema persistir:

1. Verifique a [documentação](user-guide/cli.md)
2. Use o comando [preview](user-guide/cli.md#comando-preview) para testar
3. Crie uma issue no GitHub

---

*Última atualização: 2026-04-29*