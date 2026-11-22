.PHONY: up down reset tools verify load-base dbt-build test bench logs help

help:
	@echo "Available commands:"
	@echo "  make up          - Start all docker containers in detached mode"
	@echo "  make down        - Stop all docker containers"
	@echo "  make reset       - Destructive: down -v and removes scratch data (asks confirmation)"
	@echo "  make tools       - Interactive bash shell inside the tools container"
	@echo "  make verify      - Run Stage 1 SDI verification inside tools container"
	@echo "  make load-base   - Ingest raw source files into PostgreSQL Bronze schema"
	@echo "  make dbt-build   - Run dbt build (Silver + Gold + Tests)"
	@echo "  make test        - Run pytest suite inside tools container"
	@echo "  make bench       - Run query layer benchmark harness"
	@echo "  make logs        - Tail container logs"

up:
	docker compose up -d

down:
	docker compose down

reset:
	@echo "WARNING: This will wipe PostgreSQL volumes and scratch data."
	@read -p "Are you sure? [y/N] " ans && [ $${ans:-N} = y ]
	docker compose down -v
	rm -rf data/scratch/*

tools:
	docker compose run --rm tools /bin/bash

verify:
	docker compose run --rm tools python scripts/verify_sdi.py

load-base:
	docker compose run --rm tools python scripts/load_bronze.py

dbt-build:
	docker compose run --rm tools dbt build --project-dir dbt --profiles-dir dbt

test:
	docker compose run --rm tools pytest tests/

bench:
	docker compose run --rm tools python scripts/run_bench.py

logs:
	docker compose logs -f
