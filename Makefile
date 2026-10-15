.PHONY: help install run test lint up down logs docker-run clean

PYTHON ?= python

help:
	@echo "FlightGraph development commands:"
	@echo "  make install     - Install Python dependencies"
	@echo "  make run         - Start FastAPI locally"
	@echo "  make test        - Run tests with coverage"
	@echo "  make lint        - Run Ruff and Pylint"
	@echo "  make up          - Start Docker services"
	@echo "  make down        - Stop Docker services"
	@echo "  make logs        - Display Docker logs"
	@echo "  make docker-run  - Build and start all Docker services"
	@echo "  make clean       - Remove Python caches and test artifacts"

install:
	$(PYTHON) -m pip install -r requirements.txt

PORT ?= 8000

run:
	$(PYTHON) -m uvicorn api.main:app --reload --port $(PORT)

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

docker-run:
	docker compose up -d --build --wait

clean:
	$(PYTHON) -c 'import pathlib, shutil; dirs = [p for p in pathlib.Path(".").rglob("__pycache__") if ".venv" not in p.parts]; [shutil.rmtree(p) for p in dirs]; [shutil.rmtree(p) for p in (pathlib.Path(".pytest_cache"), pathlib.Path(".ruff_cache"), pathlib.Path(".coverage_html")) if p.exists()]; pathlib.Path(".coverage").unlink(missing_ok=True)'
