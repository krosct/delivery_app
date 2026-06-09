COMPOSE ?= docker compose

.PHONY: up down logs build-db build-backend build-frontend test-backend test-frontend test run

up:
	$(COMPOSE) up --build

run: up

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f

build-db:
	$(COMPOSE) up -d db

build-backend:
	$(COMPOSE) up -d backend

build-frontend:
	$(COMPOSE) up -d frontend

test-backend:
	cd backend && pytest

test-frontend:
	npm test -- --runInBand

test: test-backend test-frontend