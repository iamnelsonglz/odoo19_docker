# ==========================
# Variables
# ==========================
COMPOSE = docker compose
PROJECT = odoo19

# ==========================
# Comandos principales
# ==========================

# Construye la imagen
build:
	$(COMPOSE) build

# Levanta todo en segundo plano
up:
	$(COMPOSE) up -d

# Apaga los servicios
down:
	$(COMPOSE) down

# Reconstruye la imagen y levanta todo
rebuild:
	$(COMPOSE) down
	$(COMPOSE) build --no-cache
	$(COMPOSE) up -d

# Muestra logs del contenedor de Odoo
logs:
	$(COMPOSE) logs -f odoo

# Entra al contenedor de Odoo
shell-odoo:
	$(COMPOSE) exec odoo bash

# Entra al contenedor de Postgres
shell-db:
	$(COMPOSE) exec db bash

# Reinicia solo Odoo (sin tocar DB)
restart-odoo:
	$(COMPOSE) restart odoo

# Limpiar contenedores, volúmenes e imágenes del proyecto
clean:
	$(COMPOSE) down -v --remove-orphans

# Reinicia todo desde cero (FULL RESET)
reset:
	$(COMPOSE) down -v --remove-orphans
	$(COMPOSE) build --no-cache
	$(COMPOSE) up -d
