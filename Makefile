# -------------------------
# Configuração de Python local (fora do Docker)
VENV = .venv
PYTHON = $(VENV)/bin/python3
REQS = requirements.txt

# -------------------------
# Target padrão
all: help  ## Target padrão: mostra a ajuda

# -------------------------
# Virtualenv local
venv: ## Cria virtualenv local e instala dependências (para rodar SEM Docker)
	@echo "🔧 Criando virtualenv e instalando dependências..."
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install -r $(REQS)
	@echo "✅ Virtualenv pronta!"

main: ## Placeholder para rodar app localmente (pode ser ajustado depois)
	@echo "ℹ Nada definido para 'main' ainda. Use 'uvicorn' ou 'docker compose up'."


clean: ## Limpa arquivos temporários locais
	@echo "🧹 Limpando arquivos temporários..."
	@rm -rf $(VENV)
	@echo "Feito!"

.PHONY: all venv main clean help

# -------------------------
# Cores/estilo (ANSI)
RESET=\033[0m
BOLD=\033[1m
DIM=\033[2m
FG_GREEN=\033[32m
FG_CYAN=\033[36m
FG_YELLOW=\033[33m
FG_RED=\033[31m
FG_BLUE=\033[34m
GRAY=\033[90m

# -------------------------
# Macros de UI
define banner
	@printf "$(FG_CYAN)$(BOLD)▶ %s$(RESET)\n" "$(1)"
endef

define ok
	@printf "$(FG_GREEN)✔ %s$(RESET)\n" "$(1)"
endef

define warn
	@printf "$(FG_YELLOW)⚠ %s$(RESET)\n" "$(1)"
endef

define fail
	@printf "$(FG_RED)✖ %s$(RESET)\n" "$(1)"
endef

# Spinner simples (gira enquanto o comando roda)
# Uso: $(call spin,Mensagem,comando args...)
define spin
	@bash -c 'set -euo pipefail; MSG=$(printf "%s" "$(1)"); \
	i=0; frames="/-\|"; printf "$(FG_BLUE)⏳ %s $(RESET)" "$$MSG"; \
	( $(2) ) & pid=$$!; \
	while kill -0 $$pid 2>/dev/null; do i=$$(( (i+1) % 4 )); printf "\r$(FG_BLUE)⏳ %s %s$(RESET) " "$$MSG" "$${frames:$$i:1}"; sleep 0.1; done; \
	wait $$pid; printf "\r$(FG_GREEN)✔ %s$(RESET)\n" "$$MSG";'
endef

# -------- Ajuda automática
# Regra: comente o target com "## descrição" na mesma linha.
help: ## Mostra esta ajuda
	@echo ""
	@printf "$(BOLD)EduTech — comandos disponíveis$(RESET)\n\n"
	@grep -E '^[a-zA-Z0-9_.-]+:.*?## ' Makefile | sed -E 's/:.*?## /: /' | sort | awk '{printf "  $(FG_CYAN)%-18s$(RESET) %s\n", $$1, substr($$0, index($$0,$$2))}'
	@echo ""


# =========================
# Docker / Docker Compose
# =========================
.PHONY: build build-log up up-b down down-v status logs

# -------- Comandos base para Docker
COMPOSE			= docker compose
DOCKER_BUILD	= $(COMPOSE) build
DOCKER_BLOG		= $(COMPOSE) up --build
DOCKER_UP		= $(COMPOSE) up -d
DOCKER_UP_B		= $(COMPOSE) up -d --build
DOCKER_DOWN		= $(COMPOSE) down
DOCKER_DOWN_V	= $(COMPOSE) down -v

build: ## Builda as imagens Docker (sem subir containers)
	$(call banner,Buildando as imagens Docker - sem subir containers)
	@$(DOCKER_BUILD)

build-log: ## Builda as imagens, sobe containers e mantém logs ativos
	$(call banner,Buildando as imagens Docker, subindo containers e mantendo logs ativos)
	@$(DOCKER_BLOG)

up: ## Sobe o PostgreSQL e FastAPI via Docker Compose
	$(call spin,Subindo containers (Docker), $(DOCKER_UP))

up-b: ## Sobe containers forçando rebuild das imagens
	$(call spin,Subindo containers (Docker) com build, $(DOCKER_UP_B))

down: ## Derruba containers (mantém volume); use 'make down-v' para reset total
	$(call spin,Derrubando containers (Docker), $(DOCKER_DOWN))

down-v: ## Derruba containers e remove volume (reset do banco)
	$(call spin,Derrubando containers e volumes (Docker), $(DOCKER_DOWN_V))

status: ## Mostra status dos serviços do Docker Compose
	$(COMPOSE) ps

logs: ## Mostra logs dos serviços do Docker Compose
	$(COMPOSE) logs -f

# =========================
# Comandos de banco (Alembic)
# =========================
.PHONY: db.revision db.migrate db.downgrade db.current db.history

db.revision: ## Cria uma nova revision com autogenerate [Uso: make db.revision msg="create users table"]
	@if [ -z "$(msg)" ]; then \
		echo "✖ Use: make db.revision msg=\"mensagem da migration\""; \
		exit 1; \
	fi
	docker compose exec backend bash -c "alembic revision --autogenerate -m '$(msg)'"

db.migrate: ## Aplica todas as migrations pendentes até o head
	docker compose exec backend bash -c "alembic upgrade head"
 
db.downgrade: ## Faz downgrade para uma revision específica [Uso: make db.downgrade rev="7c51cc8a7522"]
	@if [ -z "$(rev)" ]; then \
		echo "✖ Use: make db.downgrade rev=\"<revision_id>\""; \
		exit 1; \
	fi
	docker compose exec backend bash -c "alembic downgrade '$(rev)'"

db.current: ## Mostra a versão atual aplicada no banco
	docker compose exec backend bash -c "alembic current"

db.history: ## Mostra o histórico de migrations
	docker compose exec backend bash -c "alembic history"