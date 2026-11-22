# ADR-002: Pinned Versions for All Stack Components

- **Status**: ACCEPTED
- **Date**: 2026-11-22
- **Context**: 
  Rule 3.1 of AGENTS.md mandates strict version pinning with no use of `latest` tags to guarantee 100% reproducible environments and eliminate dependency drift.
- **Decision**:
  Pin exact compatible releases across all container images and Python packages:
  1. **PostgreSQL**: `postgres:16.4-alpine`
  2. **Apache Airflow**: `apache/airflow:2.10.5-python3.11` (with LocalExecutor)
  3. **Python Runtime**: `python:3.11-slim`
  4. **dbt**: `dbt-core==1.8.7`, `dbt-postgres==1.8.2`
  5. **Data Processing**: `pandas==2.2.3`, `openpyxl==3.1.5`, `duckdb==1.1.3`, `psycopg[binary]==3.2.3`, `matplotlib==3.9.2`, `pytest==8.3.3`, `pyyaml==6.0.2`
  6. **Prometheus**: `prom/prometheus:v2.54.1`
  7. **Pushgateway**: `prom/pushgateway:v1.9.0`
  8. **Grafana**: `grafana/grafana:11.2.0`
- **Consequences**:
  - Eliminates build-time breakages and version incompatibilities.
  - Airflow constraint file: `https://raw.githubusercontent.com/apache/airflow/constraints-2.10.5/constraints-3.11.txt`.
- **Confidence**: HIGH
