COMPOSE = docker compose -f deploy/docker-compose.yaml --env-file .env

.PHONY: up stop down logs rebuild

up:
	$(COMPOSE) up -d
stop:
	$(COMPOSE) stop
down:
	$(COMPOSE) down --rmi local
logs:
	$(COMPOSE) logs -f --tail 1000
rebuild: down up