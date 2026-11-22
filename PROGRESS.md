# PROGRESS: SDI Mart
Last updated: 2026-11-22T19:04:00Z by Antigravity Agent

## RESUME HERE (always accurate; rewrite after every step)
- Current stage/step: S0.4 Build tools image & test Docker   Status: IN PROGRESS
- What was last done (1-3 lines):
  - Created repository directories per layout.
  - S0.1: Located raw source CSV files and copied to `data/source/`, copied template to `excel/DAWH_DWH_Pharma_ColdChain_Sales_Demand-00.xlsx`, and computed SHA-256 checksums to `docs/bronze/source_checksums.txt`.
  - S0.2: Created `.gitignore`, `.env.example`, `.env`, `Makefile`. Initialized `git`.
  - S0.3: Created `docs/commands.md`, `docs/assumptions.md`, and `PROGRESS.md`.
- Exact next action (a command or file to open):
  - Create `docker/tools/Dockerfile` and `docker-compose.yml` (for tools service), then run `docker compose build tools` and test execution per S0.4.
- Environment state: containers up? (Docker daemon is running healthy; containers not yet up), DB schemas: pending S3, Airflow: pending S3.
- Known failures / things that are half-done and must not be assumed to work:
  - None. Clean bootstrap in progress.
- Open human questions (with my recommendation):
  - None. All architectural constraints resolved in AGENTS.md.

## STEP CHECKLIST
| Step | Title | Tag | Status | Evidence file | Commit |
|---|---|---|---|---|---|
| S0.1 | Locate inputs & compute SHA-256 checksums | MUST | DONE | docs/bronze/source_checksums.txt | |
| S0.2 | Create repo layout, git init, .gitignore, .env.example, Makefile | MUST | DONE | Makefile, .gitignore | |
| S0.3 | Create PROGRESS.md, docs/commands.md, docs/assumptions.md | MUST | DONE | PROGRESS.md, docs/commands.md | |
| S0.4 | Check Docker works; build & test tools image | MUST | IN PROGRESS | docs/commands.md | |
| S0.5 | Write ADR-001 (Architecture) & ADR-002 (Pinned versions) | MUST | TODO | docs/decisions/001-architecture.md | |
| S1.1 | Source inventory & data profiling | MUST | TODO | docs/sdi_verification/01_profile.md | |
| S1.2 | Test hypotheses H1-H18 with DuckDB in tools | MUST | TODO | docs/sdi_verification/02_findings.md | |
| S1.3 | Test Q1-Q3 on prototype & develop Q1'-Q3' | MUST | TODO | docs/sdi_verification/03_query_test_report.md | |
| S1.4 | Documentation risk review | SHOULD | TODO | docs/sdi_verification/05_doc_risk_review.md | |
| S1.5 | Workbook change list & generator requirements | MUST | TODO | docs/sdi_verification/04_workbook_change_list.md | |
| S1.6 | Compile Stage 1 ADRs & prove checksums unchanged | MUST | TODO | docs/decisions/ | |
| S2.1 | Copy workbook to -01 and apply change list | MUST | TODO | excel/DAWH_DWH_Pharma_ColdChain_Sales_Demand-01.xlsx | |
| S2.2 | Add Changelog sheet & update Q1'-Q3' with proof | MUST | TODO | excel/DAWH_DWH_Pharma_ColdChain_Sales_Demand-01.xlsx | |
| S2.3 | Regenerate constellation diagram & embed | MUST | TODO | constellation_diagram.png | |
| S3.1 | Finalize pinned versions in ADR-002 | MUST | TODO | docs/decisions/002-pinned-versions.md | |
| S3.2 | docker-compose.yml full stack setup | MUST | TODO | docker-compose.yml | |
| S3.3 | PostgreSQL init DDL (schemas, tables, indexes) | MUST | TODO | sql/ddl/ | |
| S3.4 | Hello-world DAG verification | MUST | TODO | dags/hello_world.py | |
| S4.1 | Source inventory document | MUST | TODO | docs/bronze/source_inventory.md | |
| S4.2 | scripts/load_bronze.py Python loader | MUST | TODO | scripts/load_bronze.py | |
| S4.3 | bronze.load_manifest idempotency | MUST | TODO | docs/bronze/load_manifest_evidence.md | |
| S4.4 | scripts/check_bronze.py validation | MUST | TODO | docs/bronze/bronze_check.md | |
| S4.5 | Loader unit & failure tests | MUST | TODO | tests/test_loader.py | |
| S5.1 | Airflow dag_mart_sdi implementation | MUST | TODO | dags/dag_mart_sdi.py | |
| S6.1 | Profile landed PostgreSQL bronze tables | MUST | TODO | docs/bronze/bronze_profile.md | |
| S6.2 | dbt-postgres project setup | MUST | TODO | dbt/dbt_project.yml | |
| S6.3 | Silver dbt models (cleaning, dedup, rejects) | MUST | TODO | dbt/models/silver/ | |
| S6.4 | Gold dbt models (conformed dims, facts) | MUST | TODO | dbt/models/gold/ | |
| S6.5 | SCD2 test fixture & point-in-time proof | MUST | TODO | data/test_fixtures/ | |
| S6.6 | dbt tests & reconciliation suite | MUST | TODO | tests/reconciliation/ | |
| S7.1 | Tagged Q1'-Q3' in sql/bench/ on Gold | MUST | TODO | sql/bench/ | |
| S7.2 | Q1'-Q3' reconciliation to raw data | MUST | TODO | docs/q_acceptance.md | |
| S7.3 | SK-misuse prevention test | MUST | TODO | tests/test_sk_misuse.py | |
| S8.1 | Prometheus & Pushgateway metric publisher | MUST | TODO | include/observability/ | |
| S8.2 | Provisioned Grafana Ingestion Dashboard | MUST | TODO | config/grafana/dashboards/ | |
| S8.3 | Ingestion metric dictionary | MUST | TODO | docs/metrics_ingestion.md | |
| S9.1 | Canonical query catalogue (>= 10 queries, 4 pages) | MUST | TODO | sql/bench/ | |
| S9.2 | Benchmark harness scripts/run_bench.py | MUST | TODO | scripts/run_bench.py | |
| S9.3 | Baseline benchmark execution & query_log | MUST | TODO | docs/query_optimization.md | |
| S9.4 | Query optimization & measured speed-ups | MUST | TODO | docs/query_optimization.md | |
| S9.5 | Provisioned Grafana Query Performance Dashboard | MUST | TODO | config/grafana/dashboards/ | |
| S10.1| Clean-clone reproduction test | MUST | TODO | docs/clean_clone_test.md | |
| S10.2| Comprehensive README.md | MUST | TODO | README.md | |
| S10.3| SDI metric dictionary | SHOULD | TODO | docs/metrics.md | |
| S10.4| Generator spec stub for SDI | SHOULD | TODO | docs/sdi_verification/06_generator_requirements.md | |
| S10.5| Final PROGRESS.md & git tag iter-sdi-v01 | MUST | TODO | PROGRESS.md | |

## STAGE LOG (append-only, newest at bottom)
### S0.1 - S0.3: Bootstrap Scaffolding
- Plan: Create directories, copy source CSVs and template workbook, compute SHA-256 hashes, generate .gitignore, .env.example, Makefile, commands.md, assumptions.md, PROGRESS.md.
- Commands run + result:
  - Copy-Item: 7 CSV files to `data/source/`, template to `excel/DAWH_DWH_Pharma_ColdChain_Sales_Demand-00.xlsx`.
  - Get-FileHash: 8 SHA-256 hashes stored in `docs/bronze/source_checksums.txt`.
- Decisions/ADRs:
  - ADR-001 (Architecture) created.
- Assumptions:
  - A-01 through A-06 logged in `docs/assumptions.md`.
- Evidence files:
  - `docs/bronze/source_checksums.txt`
  - `.gitignore`, `.env.example`, `Makefile`, `docs/commands.md`, `docs/assumptions.md`

## DECISIONS INDEX
- ADR-001: Target architecture (dbt-postgres, PostgreSQL bronze/silver/gold, Airflow direct loader, DuckDB verification only).
- ADR-002: Pinned versions for all Docker components (Airflow 2.10.5, Postgres 16.4, dbt-core 1.8.7, dbt-postgres 1.8.2, Prometheus 2.54.1, Pushgateway 1.9.0, Grafana 11.2.0, Python 3.11).

## ASSUMPTIONS INDEX
- A-01: CSV & Excel dual ingestion support.
- A-02: Target transformation engine is PostgreSQL via dbt-postgres.
- A-03: Grafana + Prometheus containerized observability.
- A-04: 4 US regions derived from State codes.
- A-05: Single point-in-time master data; SCD2 demonstrated via controlled test fixture.
- A-06: Blank cells ingested as SQL NULL in bronze.

## KNOWN RISKS TO 25 NOV
- Scope containment: strictly enforce Section 12 (no Superset, no 24/7 simulator, no Phases 2/3) to finish Query Layer by 25 Nov.
