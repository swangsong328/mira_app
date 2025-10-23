.PHONY: help dev migrate seed test clean up down shell logs format lint check install

help:
	@echo "Beauty Salon MVP - Available Commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make dev        - Run development server locally"
	@echo "  make migrate    - Run database migrations"
	@echo "  make seed       - Seed demo data"
	@echo "  make test       - Run test suite"
	@echo "  make format     - Format code (black + isort)"
	@echo "  make lint       - Run linters (ruff + mypy)"
	@echo "  make check      - Run format + lint + test"
	@echo "  make up         - Start Docker Compose services"
	@echo "  make down       - Stop Docker Compose services"
	@echo "  make shell      - Open Django shell"
	@echo "  make logs       - View Docker logs"
	@echo "  make clean      - Clean cache and temp files"

install:
	pip install -r requirements.txt

dev:
	python manage.py runserver

migrate:
	python manage.py makemigrations
	python manage.py migrate

seed:
	python manage.py seed_demo

test:
	pytest

format:
	black .
	isort .

lint:
	ruff check .
	mypy .

check: format lint test

up:
	docker-compose up -d

down:
	docker-compose down

shell:
	python manage.py shell

logs:
	docker-compose logs -f web

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov .coverage


