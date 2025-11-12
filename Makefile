VENV = venv
PYTHON = $(VENV)/bin/python3
REQS = requirements.txt

all: main

venv:
	@echo "🔧 Criando virtualenv e instalando dependências..."
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install -r $(REQS)
	@echo "✅ Virtualenv pronta!"

main:


clean:
	@echo "🧹 Limpando arquivos temporários..."
	@echo "Feito!"
