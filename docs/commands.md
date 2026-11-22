# Commands Guide & Environment Runbook

## Docker Lifecycle
```bash
# Start all platform containers
docker compose up -d

# Check health and running status
docker compose ps

# View container logs
docker compose logs -f [service_name]

# Stop platform containers
docker compose down
```

## Stage 0 & Stage 1: Verification
```bash
# Build the tools container image
docker compose build tools

# Run Stage 1 SDI Verification inside tools container
docker compose run --rm tools python scripts/verify_sdi.py

# Re-run benchmark queries inside tools container
docker compose run --rm tools python scripts/run_bench.py
```

## Stage 4: Ingestion to Bronze
```bash
# Ingest raw source files into PostgreSQL bronze schema
docker compose run --rm tools python scripts/load_bronze.py

# Verify bronze row counts and metadata
docker compose run --rm tools python scripts/check_bronze.py
```

## Stage 6: dbt Transformations (Silver & Gold)
```bash
# Test dbt connection
docker compose run --rm tools dbt debug --project-dir dbt --profiles-dir dbt

# Run dbt snapshot (SCD Type 2)
docker compose run --rm tools dbt snapshot --project-dir dbt --profiles-dir dbt

# Run full dbt build (Silver + Gold + Tests)
docker compose run --rm tools dbt build --project-dir dbt --profiles-dir dbt
```

## Access Endpoints
- **Airflow Web UI**: http://localhost:8080 (User: `admin` / Password: `admin`)
- **Grafana Dashboards**: http://localhost:3000 (User: `admin` / Password: `admin`)
- **Prometheus UI**: http://localhost:9090
- **Pushgateway UI**: http://localhost:9091
- **PostgreSQL Database**: `localhost:5433` (DB: `dwh`, User: `pharma_admin`)
