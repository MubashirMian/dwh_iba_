# Pharmaceutical Cold-Chain Data Warehouse & BI Pipeline
## Phase 1: Sales & Demand Intelligence (SDI) Mart

[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16.4-336791?logo=postgresql)](https://www.postgresql.org/)
[![dbt](https://img.shields.io/badge/dbt-1.8.7-FF694B?logo=dbt)](https://www.getdbt.com/)
[![Airflow](https://img.shields.io/badge/Apache_Airflow-2.10.5-017CEE?logo=apacheairflow)](https://airflow.apache.org/)
[![Grafana](https://img.shields.io/badge/Grafana-11.2.0-F46800?logo=grafana)](https://grafana.com/)
[![Prometheus](https://img.shields.io/badge/Prometheus-2.54.1-E6522C?logo=prometheus)](https://prometheus.io/)

---

### 1. Architecture Overview
This repository implements an enterprise-grade, containerized Medallion Architecture data warehouse designed to optimize pharmaceutical supply chain resilience, monitor cold-chain compliance, eliminate hospital drug stockouts, and analyze commercial margins.

```mermaid
flowchart LR
    A["Raw Sources (.csv / .xlsx)"] --> B["Bronze Layer (PostgreSQL)"]
    B --> C["Silver Layer (dbt Views)"]
    C --> D["Gold Star Schema (PostgreSQL)"]
    D --> E["Query Layer & Grafana BI"]
    
    subgraph Observability
        B -. Ingestion Metrics .-> P[Pushgateway] --> PR[Prometheus] --> G[Grafana]
        D -. obs.query_log .-> G
    end
```

### 2. Medallion Layers
- **Bronze Layer (`bronze.*`)**: High-performance COPY protocol loader storing raw fidelity text with technical audit columns (`_loaded_at`, `_source_file`, `_row_id`) and cryptographic SHA-256 manifest tracking (`bronze.load_manifest`).
- **Silver Layer (`silver.*`)**: Modular dbt views handling type casting, date parsing, whitespace/null cleaning, deduplication, and quality filters.
- **Gold Layer (`gold.*`)**: Star Schema constellation mart:
  - `dim_date`: 1,461 calendar days (2023–2026).
  - `dim_medicine`: 63 SKUs with Slowly Changing Dimension Type 2 (SCD2) versioning.
  - `dim_facility`: 72 conformed facilities (50 commercial pharmacies + 12 hospital dispensaries across 4 US regions).
  - `dim_warehouse`: 6 regional distribution centers.
  - `dim_sales_profile`: 1,441 transaction profile combinations.
  - `fact_pharm_sales`: 500,000 transaction line items ($37.98M net revenue).
  - `fact_demand`: 27,216 monthly hospital demand records (20.4M clinical units).
  - `fact_inventory`: 112,184 lot-level daily warehouse snapshots.

### 3. Key Analytical Queries (Q1' - Q3')
- **Q1' (Monthly Sales vs Hospital Demand)**: Compares commercial pharmacy sell-through vs clinical demand fulfillment by region and disease category, calculating true hospital fill rate without double-counting.
- **Q2' (Stockout & Expiry Exposure)**: Identifies top-velocity medicines facing imminent expiration (<90 days) or active stockouts, joined across facts on natural key `medicine_id` to eliminate SCD2 version splitting.
- **Q3' (Commercial Profitability)**: Calculates gross sales, discount penetration, COGS, gross margin, return rates, and volume-weighted remaining shelf-life (`PackWeightedAvgDaysToExpiry`).

### 4. Live Services & Endpoints
| Service | URL | Credentials | Purpose |
|---|---|---|---|
| **Grafana Dashboard** | [http://localhost:3000](http://localhost:3000) | `admin` / `admin` | Real-time ingestion & query latency monitoring |
| **Airflow UI** | [http://localhost:8080](http://localhost:8080) | `admin` / `admin` | Pipeline DAG orchestration |
| **Prometheus** | [http://localhost:9090](http://localhost:9090) | *None* | Metric scraping and time-series database |
| **Pushgateway** | [http://localhost:9091](http://localhost:9091) | *None* | Ingestion job metric buffer |
| **PostgreSQL DWH** | `localhost:5432` (`dwh`) | `pharma_admin` / `pharma_secret_pw` | Warehouse database |

### 5. Automated Testing & Verification
The warehouse includes a complete suite of automated validations:
- **dbt Test Suite**: 22 data tests covering unique constraints, not-null rules, and foreign key relationships.
- **SCD2 Point-in-Time Fixture**: `tests/test_scd2_fixture.py` proving historical transaction resolution.
- **SK-Misuse Prevention**: `tests/test_sk_misuse.py` enforcing natural key joins across fact grains.
- **Observability Audit**: Every query execution is benchmarked and logged into `obs.query_log`.
