# ADR-001: Target Architecture & Component Technology Selection

- **Status**: ACCEPTED
- **Date**: 2026-11-22
- **Context**: 
  The project requires an automated Data Warehouse and BI pipeline for a Pharmaceutical Cold Chain distribution network across 7 datasets. Prior project documents had minor conflicts between using DuckDB vs PostgreSQL for the transformation and dimensional serving layer.
- **Decision**:
  1. **Transformation & Mart Engine**: `dbt-postgres` running in PostgreSQL 16. Schemas: `bronze` (raw untransformed text), `silver` (cleaned, typed, deduped), `gold` (Kimball star schema / constellation marts, pre-aggregates), `obs` (observability logs), and `dq` (data quality rejects).
  2. **DuckDB Role**: Strictly an ad-hoc exploratory verification SQL engine over source CSVs (`read_csv_auto`) in Stage 1 within the containerized `tools` environment. It is never used as the production Bronze layer or the dbt target.
  3. **Ingestion Mechanism**: Apache Airflow 2.10.x orchestrates the ingestion via task `load_excel_to_postgres_bronze` executing a robust Python loader (`include/ingestion/`).
  4. **Observability Stack**: Ingestion throughput/latency/error metrics emitted to Prometheus via Pushgateway, rendered in Grafana. Query layer benchmark metrics logged to PostgreSQL `obs.query_log`, visualized via a dedicated Grafana PostgreSQL datasource.
- **Consequences**:
  - Ensures 100% compatibility with standard dbt SQL modeling.
  - Eliminates DuckDB concurrency lock traps (single-writer constraint) when multiple dashboard visual queries run simultaneously.
  - Fully supports Dockerized execution under an 8 GB RAM constraint.
- **Confidence**: HIGH
