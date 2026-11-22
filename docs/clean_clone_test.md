# Clean-Clone Reproduction Test Guide

This document certifies that the **Pharma Cold-Chain DWH (Phase 1 SDI Mart)** is fully reproducible from scratch on any machine with Docker installed.

## 1. Prerequisites
- Docker Engine & Docker Compose (v2.20+)
- Git

## 2. Reproduction Steps
```powershell
# 1. Clone repository
git clone <repo-url> pharma_dwh
cd pharma_dwh

# 2. Boot Core Infrastructure (PostgreSQL, Prometheus, Pushgateway, Grafana)
docker compose up -d postgres pushgateway prometheus grafana

# 3. Ingest Bronze Layer (All 7 Raw Datasets)
docker compose run --rm tools python scripts/load_bronze.py --force

# 4. Transform Bronze -> Silver (Views) -> Gold (Star Schema) via dbt
docker compose run --rm tools bash -c "cd dbt && dbt run --profiles-dir ."

# 5. Execute 22 Automated Data Integrity Tests
docker compose run --rm tools bash -c "cd dbt && dbt test --profiles-dir ."

# 6. Run Analytical Queries & Observability Benchmarks (Q1' - Q3')
docker compose run --rm tools bash -c "python scripts/run_bench.py && python tests/test_scd2_fixture.py && python tests/test_sk_misuse.py"

# 7. Apply Query Optimizations (B-Tree Indexes)
docker compose run --rm tools python scripts/optimize_gold.py
```

## 3. Verification URLs
- **Grafana Live Observability Dashboard**: [http://localhost:3000](http://localhost:3000) (Login: `admin` / `admin`)
- **Prometheus Metrics**: [http://localhost:9090](http://localhost:9090)
- **Pushgateway Ingestion Metrics**: [http://localhost:9091](http://localhost:9091)
- **Airflow Web UI**: [http://localhost:8080](http://localhost:8080) (Login: `admin` / `admin`)
