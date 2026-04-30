# Instalação

Este guia detalha todos os passos necessários para instalar e configurar o Video Clips Automation no seu computador.

## Pré-requisitos

Antes de iniciar a instalação, certifique-se de ter os seguintes requisitos atendidos:

### Requisitos Obrigatórios

| Requisito | Versão Mínima | Descrição |
|-----------|---------------|-----------|
| Python | 3.10 ou superior | Linguagem de programação |
| FFmpeg | Qualquer versão recente | Processamento de vídeo e áudio |
| Espaço em disco | 2 GB livres | Para dependências e vídeos |

### Sistemas Operacionais Suportados

- **Windows** 10 ou 11
- **macOS** 10.14 (Mojave) ou superior
- **Linux** (Ubuntu 20.04+, Debian 10+, Fedora 34+)

### Dependências Externas

O Video Clips Automation depende dos seguintes componentes:

| Componente | Necessário | Descrição |
|------------|-----------|-----------|
| FFmpeg | Sim | Processamento de vídeo e áudio |
| OpenCV | Sim | Análise visual de quadros |
| Whisper | Opcional | Geração de legendas automáticas |

---

## Instalação do Python

### Windows

1. Acesse o site oficial: [python.org](https://www.python.org/downloads/)
2. Baixe a versão mais recente (3.10 ou superior)
3. Execute o instalador
4. **Importante**: Marque a opção "Add Python to PATH"

Verifique a instalação:

```bash
python --version
```

### macOS

Você pode instalar o Python de várias formas:

**Opção 1: Homebrew (Recomendado)**

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python
```

**Opção 2: Installer Oficial**

1. Acesse [python.org/downloads/mac-osx/](https://www.python.org/downloads/mac-osx/)
2. Baixe o instalador para a sua versão do macOS
3. Execute o pkg e siga as instruções

Verifique a instalação:

```bash
python3 --version
```

### Linux

**Debian/Ubuntu:**

```bash
sudo apt update
sudo apt install python3.10 python3-pip ffmpeg
```

**Fedora:**

```bash
sudo dnf install python310 python-pip ffmpeg
```

**Arch Linux:**

```bash
sudo pacman -S python python-pip ffmpeg
```

Verifique a instalação:

```bash
python3 --version
```

---

## Instalação do FFmpeg

O FFmpeg é essencial para o processamento de vídeo.

### Windows

**Opção 1: Binários Pré-compilados**

1. Acesse [ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Baixe a versão "essentials" para Windows
3. Extraia o arquivo ZIP
4. Adicione a pasta `bin` ao PATH do sistema

**Opção 2: Chocolatey**

```powershell
choco install ffmpeg
```

**Opção 3: Winget**

```powershell
winget install FFmpeg.FFmpeg
```

Verifique a instalação:

```bash
ffmpeg -version
```

### macOS

```bash
brew install ffmpeg
```

### Linux

**Debian/Ubuntu:**

```bash
sudo apt install ffmpeg
```

**Fedora:**

```bash
sudo dnf install ffmpeg
```

---

## Clonando o Repositório

Clone o repositório do projeto ou baixe o código-fonte:

```bash
git clone https://github.com/user/clips_videos.git
cd clips_videos
```

Se você não tem o Git instalado, baixe o código como ZIP:
[Baixar Código](https://github.com/user/clips_videos/archive/refs/heads/main.zip)

---

## Configuração do Ambiente Virtual

É altamente recomendável usar um ambiente virtual para evitar conflitos com outras instalações Python.

### Criando o Ambiente Virtual

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Após ativar, você verá o prefixo `(.venv)` no seu terminal.

### Saindo do Ambiente Virtual

Quando terminar de usar, saia com o comando:

**Windows:**

```bash
.venv\Scripts\deactivate.bat
```

**macOS/Linux:**

```bash
deactivate
```

---

## Instalando as Dependências

Com o ambiente virtual ativo, instale todas as dependências:

```bash
pip install -r requirements.txt
```

### Lista de Dependências Principais

O arquivo `requirements.txt` inclui:

| Pacote | Descrição |
|--------|-----------|
| opencv-python | Processamento de imagens e vídeo |
| moviepy | Edição de vídeo |
| whisper | Transcrição de áudio |
| click | Interface de linha de comando |
| numpy | Cálculos numéricos |
| PyQt6 | Interface gráfica |

### Verificando a Instalação

Após a instalação, verifique se tudo está correto:

```bash
python -m src.cli.commands --version
```

Você deverá ver:

```
Video Clips Automation, version 1.0.0
```

---

## Instalação de Dependências Opcionais

### Para Legendas Automáticas (Whisper)

O Whisper é instalado automaticamente, mas você pode escolher um modelo diferente:

| Modelo | Tamanho | Precisão |
|---------|---------|----------|
| tiny | 39 MB | Boa |
| base | 74 MB | Muito boa |
| small | 244 MB | Excelente |
| medium | 769 MB | Excelente |
| large | 1550 MB | Melhor |

Para usar um modelo específico, configure no arquivo de configuração:

```json
{
  "subtitles": {
    "whisper_model": "small"
  }
}
```

### Para Interface Gráfica (GUI)

A GUI requer PyQt6, que já está no requirements.txt:

```bash
pip install PyQt6
```

---

## Configuração Inicial

Após a instalação, você pode criar um arquivo de configuração inicial:

```bash
python -m src.cli.commands init-config
```

Isso criará um arquivo `config.example.json` com todas as opções disponíveis.

---

## Testando a Instalação

Execute um teste simples para verificar que tudo está funcionando:

```bash
python -m src.cli.commands preview video_exemplo.mp4
```

Substitua `video_exemplo.mp4` por um arquivo de vídeo válido no seu computador.

---

## Próximos Passos

Agora que você tem tudo instalado, siga para:

- **[Guia Rápido](quick-start.md)** - Primeiro processamento
- **[Interface CLI](../user-guide/cli.md)** - Comandos disponíveis
- **[Exemplos Práticos](../examples/index.md)** - Casos de uso

---

## Problemas na Instalação?

Se encontrar algum erro, consulte a página de **[Solução de Problemas](../troubleshooting.md)**.

---

*Última atualização: 2026-04-29*