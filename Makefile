# Makefile - Comandos Úteis

# Cores
GREEN = \033[0;32m
YELLOW = \033[0;33m
BLUE = \033[0;34m
RESET = \033[0m

# Variáveis
PYTHON = python
PIP = pip
VENV_ACTIVATE = .venv\Scripts\activate.bat
SRC = src
TESTS = tests

# Targets
.PHONY: help install test lint format clean run gui config

help:
	@echo "$(BLUE)Video Clips Automation - Comandos Úteis$(RESET)"
	@echo ""
	@echo "make install    - Instalar dependências"
	@echo "make test      - Executar testes"
	@echo "make lint     - Verificar código com flake8"
	@echo "make format  - Formatar código com black"
	@echo "make clean   - Limpar arquivos temporários"
	@echo "make run     - Executar CLI"
	@echo "make gui    - Abrir interface GUI"
	@echo "make config - Criar config exemplo"

install:
	@echo "$(GREEN)Instalando dependências...$(RESET)"
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)✓ Instalação concluída$(RESET)"

test:
	@echo "$(GREEN)Executando testes...$(RESET)"
	$(PYTHON) -m pytest $(TESTS) -v

test-unit:
	@echo "$(GREEN)Executando testes unitários...$(RESET)"
	$(PYTHON) -m pytest $(TESTS)/unit -v

test-integration:
	@echo "$(GREEN)Executando testes de integração...$(RESET)"
	$(PYTHON) -m pytest $(TESTS)/integration -v

test-coverage:
	@echo "$(GREEN)Executando testes com coverage...$(RESET)"
	$(PYTHON) -m pytest $(TESTS) --cov=$(SRC) --cov-report=html --cov-report=term

lint:
	@echo "$(GREEN)Verificando código...$(RESET)"
	$(PYTHON) -m flake8 $(SRC) --max-line-length=100 --ignore=E203,W503

format:
	@echo "$(GREEN)Formatando código...$(RESET)"
	$(PYTHON) -m black $(SRC) --line-length=100

clean:
	@echo "$(GREEN)Limpando arquivos temporários...$(RESET)"
	$(PYTHON) -m clean --all
	@echo "$(GREEN)✓ Limpeza concluída$(RESET)"

run:
	@echo "$(GREEN)Executando CLI...$(RESET)"
	$(PYTHON) -m $(SRC).cli.commands

gui:
	@echo "$(GREEN)Abrindo GUI...$(RESET)"
	$(PYTHON) -m $(SRC).cli.commands gui

config:
	@echo "$(GREEN)Criando config exemplo...$(RESET)"
	$(PYTHON) -m $(SRC).cli.commands init-config -o configs/config.example.json

preview:
	@echo "$(GREEN)Gerando preview...$(RESET)"
	$(PYTHON) -m $(SRC).cli.commands preview

dev-install:
	@echo "$(GREEN)Instalando para desenvolvimento...$(RESET)"
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-cov black flake8 mypy pre-commit
	@echo "$(GREEN)✓ Instalação concluída$(RESET)"

check:
	@echo "$(GREEN)Verificando código...$(RESET)"
	$(PYTHON) -m black --check $(SRC)
	$(PYTHON) -m flake8 $(SRC) --max-line-length=100
	$(PYTHON) -m mypy $(SRC)
	@echo "$(GREEN)✓ Verificação concluída$(RESET)"