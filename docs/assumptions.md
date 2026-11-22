# Project Assumptions & Design Decisions

This document tracks all operational, business, and architectural assumptions across the Pharma Cold Chain Data Warehouse project.

| ID | Stage | Assumption | Rationale | Impact |
|---|---|---|---|---|
| A-01 | S0 | Source files are provided as `.csv` files alongside a consolidated `.xlsx` workbook. Ingestion pipeline accepts both `.csv` and `.xlsx`. | The assignment text refers to "Excel files" while the provided dataset contains individual `.csv` files. | Ingestion loader (`load_bronze.py`) supports both formats seamlessly. |
| A-02 | S0 | Target transformation engine is PostgreSQL via `dbt-postgres`. | Resolves previous contradiction with DuckDB: dbt models run natively in PostgreSQL to populate schemas `silver` and `gold`. | DuckDB is restricted to Stage 1 verification discovery only. |
| A-03 | S0 | Power BI / Grafana split: Grafana monitors pipeline ingestion (Prometheus) and query performance (`obs.query_log`). Business BI runs in Superset / Power BI. | Follows spec guidelines and avoids desktop-only constraints inside Docker. | Observability runs 100% containerized with zero manual steps. |
| A-04 | S1 | 4 US Regions (Northeast, Midwest, South, West) are derived from `State` codes across facilities and warehouses. | Geographic regional reporting is required for Q1 and Q2. | Mapping table implemented in dbt seeds/macros with 100% coverage. |
| A-05 | S1 | In the base dataset, `01_master_data.csv` represents a single point-in-time snapshot. Controlled test fixtures provide SCD2 versioning evidence. | To demonstrate Kimball SCD Type 2 point-in-time lookups without fabricating raw sources. | Ingested as a separate batch with new timestamps in Stage 6. |
| A-06 | S4 | In Bronze layer, empty spreadsheet cells and blank CSV fields are ingested as SQL `NULL`. | Preserves raw schema fidelity without premature transformation. | Handled explicitly in Silver cleaning layer. |
