.PHONY: help test lint up down logs

PYTHON ?= python

help:
	@echo "FlightGraph development commands:"
	@echo "  make test  - Run tests with coverage"
	@echo "  make lint  - Run Ruff and Pylint"
	@echo "  make up    - Start Docker services"
	@echo "  make down  - Stop Docker services"
	@echo "  make logs  - Display Docker logs"

test:
	$(PYTHON) -m pytest --cov=api --cov-report=term-missing

lint:
	$(PYTHON) -m ruff check api/ tests/
	$(PYTHON) -m pylint api/ --fail-under=9.5

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f
