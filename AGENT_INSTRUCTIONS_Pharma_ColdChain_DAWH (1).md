# Pharma Cold-Chain DWH + BI Pipeline: AI Agent Instruction Set

**Version 1.0 · written 22 Nov 2026 · Course: Data Analytics & Warehousing (Fall 2026)**
**Stack:** Docker · Airflow · FastAPI + file-watcher · Postgres (ODS) · DuckDB (marts) · dbt · Superset + Grafana · Medallion + Semantic Layer

---

## 0. How to use this file

| Part | Audience | Use |
|---|---|---|
| **A**: Requirement analysis | You (student) | Read first. Confirm the flagged ambiguities with the instructor. |
| **B**: Agent constitution | The AI agent | Save as `AGENTS.md` (or `CLAUDE.md`) in the repo root. The agent reads it at the start of every session. |
| **C**: Iterations 0-10 | The AI agent | Paste **one iteration at a time** as the task prompt (template in Appendix). Never start iteration N+1 until N's Definition of Done passes. |
| **D-F**: Design starting points | The AI agent | Dimensional model, semantic layer, inventory-solution spec. Always **validate against real data profiling** before trusting them. |
| **G**: Demo and report checklist | Both | Used in the last iteration, but fed incrementally from Iteration 1. |

"Meta dillion" is read as **Medallion** (Bronze → Silver → Gold). If you meant something else, tell the agent in Iteration 0.

---

# PART A: REQUIREMENT ANALYSIS

## A1. What is actually being graded (30% + bonus)

| Rubric item | Weight | What the grader must *see* | Evidence the agent must produce |
|---|---|---|---|
| Oversampling (generator + Airflow DAG + 1-2 page PDF) | 2% | New rows in all 7 sources; generation modeled as a DAG; methodology and stats report | `dag_generate_data`, `reports/data_generation_report.pdf`, `obs.generation_log` |
| Batch-ingestion dashboard | 2% | Load duration, rows/batch, success rate, horizontal bar of duration per source | Grafana/Superset dashboard on `obs.batch_load_log` |
| Streaming-ingestion dashboard | 2% | Throughput, E2E latency, malformed count, line chart over time | Dashboard on `obs.stream_metrics` |
| Storage dashboard | 2% | Row counts, size (MB), date-coverage, donut/stacked bar by 7 domains | Dashboard on `obs.storage_snapshot`, `obs.date_coverage` |
| Query-layer dashboard | 2% | Query time, daily query count, error rate, avg time per widget | Dashboard on `obs.query_log` + optimization before/after evidence |
| "Excel file" Phase 1 / 2 / 3 | 3 × 2.5% | **Design workbook per phase** (resolved, see A2 #2): dimension tabs, one tab per fact, star-schema/constellation diagram, and 3 solvable dimensional queries with proof | `excel/DAWH_DWH_Pharma_ColdChain_<Mart>_<NN>.xlsx`, kept in sync with the dbt models |
| Transformation + dimensional modeling | 2.5% | Star schemas, SCD, junk and role-playing dims, fact-table types | dbt project, ERDs, bus matrix |
| BI | 10% | Dashboards that **visibly change** after each refresh; each tells a story | Superset dashboards, report narrative |
| Bonus (Phase 4) | 3% (spec also says 4%) | Constellation that **solves the inventory-management problem**; master DAG; unified DE dashboard | Part F + Iteration 9 |
| Grading criteria | n/a | GitHub repo; **modular** DAG files; live demo; report with all assumptions and dashboard stories | Part G |

**The one-line summary of the whole project:** *prove a historical, incremental, automated DWH, with dashboards that visibly change after each of two refreshes, and measure every pipeline layer.*

## A2. Ambiguities, default assumptions, and what to confirm

| # | Issue in the spec | Default assumption (agent proceeds with this) | Confirm with instructor |
|---|---|---|---|
| 1 | Sources are `.csv` but text says "Excel files" | Ingest both `.csv` and `.xlsx`. The generator emits CSV deltas plus an optional XLSX copy. The watcher handles both | Which format is expected at demo? |
| 2 | Marks list "Excel file Phase 1/2/3: 2.5%" | **Resolved by the student's Phase 1 workbook (`DAWH_DWH_Pharma_ColdChain_Sales_Demand-00.xlsx`)**: tabs `Dim.Tables`, `Fact.Table.PharmSales`, `Fact.Table.Inventory`, `Fact.Table.Demand`, `Star.Schema`; the Star.Schema tab holds the constellation diagram plus **"3 Solvable Dimensional Queries"** (English query + "prove it solves the business problem"). Phases 2 and 3 reuse the same layout. Optional extra tabs: Source-to-Target, DQ rules, KPI dictionary, Assumptions | Only confirm the *Phase 2/3 mart names and expected query count* |
| 3 | Bonus is "3%" in the header and "4%" in Phase 4 | Treat as 3-4% and build it fully | Which figure is right? |
| 4 | "Streaming" ingestion, but Airflow is not a stream processor and Phase 3 allows 1-5 min micro-batches | Micro-batch, with the stream source a rate-controlled producer. The consumer measures per-event latency. Redpanda/Kafka is an optional stretch | Is micro-batch acceptable as "streaming"? |
| 5 | Power BI / Grafana / Superset allowed | **Superset** for business BI, **Grafana** for DE observability. Power BI Desktop cannot run in Docker | None needed |
| 6 | "Refreshed twice" per mart and for the constellation | Two refresh cycles **R1, R2**, forward in time (see Iteration 3), then both are re-run for the constellation | Does the constellation need *two more* refreshes? Assume yes |
| 7 | "Implement an API for ingestion" | FastAPI service (`ingest-api`) that the file-watcher calls | None needed |
| 8 | "Date coverage 2023-2025 fully represented" vs generating new data | New data extends **past 2025 (2026 H1)**. The coverage check reports both the base range and the extension | None needed, but document it |
| 9 | Phase 1 M1 deadline (11 Nov) is already past | Iteration 0 **audits existing work** and skips completed tasks | Is anything already built? Tell the agent |

## A3. Timeline reality check (today = Sun 22 Nov 2026)

- **Phase 1 Milestone 2 is due Wed 25 Nov, 3 days away.** That means the *entire* vertical slice (platform → ingestion → generator → Phase 1 mart → query layer → BI → 2 refreshes) must exist in ~72 hours. Iterations 0-6 are therefore written as a **compressed sprint with MUST / SHOULD / COULD tags**. If behind, drop SHOULD/COULD items, never MUST.
- Phase 2 due **5 Dec**, Phase 3 due **14 Dec**, constellation after that (date unspecified; assume ~late Dec).
- **Do not leave the constellation to the end.** Conformed dimensions, the metric dictionary, and the semantic layer are built *incrementally* in every phase (Iterations 4, 7, 8), so Iteration 9 is integration rather than invention.

| Iteration | Window | Milestone |
|---|---|---|
| 0 Discovery and state audit | 22 Nov | n/a |
| 1 Docker platform | 22 Nov | n/a |
| 2 Ingestion + Bronze + batch observability | 22-23 Nov | n/a |
| 3 Data generator + generation DAG | 23 Nov | n/a |
| 4 Silver/Gold Phase 1 (SDI mart) | 23-24 Nov | n/a |
| 5 Query layer + optimization | 24 Nov | n/a |
| 6 BI Phase 1 + 2 refreshes | 24-25 Nov | **P1 M2: 25 Nov** |
| 7 Phase 2: Inventory / Expiry / Replenishment | 26 Nov-5 Dec | **P2: 5 Dec** |
| 8 Phase 3: Traceability / IoT | 6-14 Dec | **P3: 14 Dec** |
| 9 Constellation + semantic layer + inventory solution | after 14 Dec | Bonus |
| 10 Hardening, observability unification, report, demo | final | Submission |

## A4. Architecture decisions (and why)

```
                    ┌────────────── Airflow (orchestration, retries, SLAs, lineage) ──────────────┐
                    │                                                                              │
 Generator ──► /data/landing ──► file-watcher ──► ingest-api ──► POSTGRES  bronze (ODS/staging)    │
 (DAG task)   batch/*.csv|xlsx   (watchdog)       (FastAPI)       + ctl (manifest) + obs (metrics) │
              stream/*.jsonl                                           │                           │
                                                                       ▼  DuckDB ATTACH (postgres) │
                                                        dbt-duckdb:  SILVER (clean, typed, conformed, SCD2)
                                                                       ▼
                                                        GOLD (star schemas → fact constellation, agg_* tables)
                                                                       ▼
                                                        SEMANTIC (sem_* views + MetricFlow metrics)
                                                                       ▼
                                               publish read-only SERVING snapshot (atomic swap)
                                                                       ▼
                                     Superset (business BI)          Grafana (DE observability on obs.*)
```

| Decision | Choice | Reasoning |
|---|---|---|
| Medallion mapping | **Bronze** = immutable raw files in `/data/archive` + Postgres `bronze` ODS tables (spec mandates Postgres staging). **Silver** = cleaned/typed/conformed/deduped (DuckDB). **Gold** = dimensional marts + aggregates (DuckDB). **Semantic** = business-named views + governed metrics | Maps the course's layers onto a recognised pattern without breaking the spec |
| Marts engine | DuckDB via **dbt-duckdb**, reading Bronze through `ATTACH ... (TYPE postgres, READ_ONLY)` | Spec-endorsed; avoids a second copy of raw data |
| **DuckDB concurrency trap** | One writer process **or** many read-only processes, never both on one file. So dbt writes `/data/warehouse/dwh.duckdb`; after each successful run a `publish_serving` task checkpoints and copies to a temp file, then `os.replace()` → `/data/serving/dwh_serving.duckdb`. Superset mounts `/data/serving` **read-only** | Without this, dashboards break during every refresh. This is the most likely demo-day failure |
| Orchestration | Airflow with LocalExecutor, **one DAG per concern**, cross-DAG dependencies via Assets/Datasets (see rule B3.7) | Meets "modular DAGs with clean task separation" |
| Ingestion | Decoupled: the **watcher** ingests on file arrival; Airflow *observes* via `ctl.batch_manifest` and proceeds | Satisfies "automated file-watcher" **and** Airflow-centric orchestration |
| BI split | Superset for business dashboards, Grafana for operational metrics from Postgres `obs` | Each tool where it is strongest. Both are allowed by the spec |
| Semantic layer | `sem_*` views + dbt **MetricFlow** metric definitions as the single source of metric truth. Superset datasets point *only* at `sem_*` | Consistent KPIs across dashboards. Cube.dev is an optional stretch |

---

# PART B: AGENT CONSTITUTION (save as `AGENTS.md`)

## B1. Role
You are a senior Data Engineer / BI engineer building a Master's-level DWH+BI project. Your output is graded on correctness, reproducibility, modular design, and **demonstrable live behaviour**. Optimise for a **working, observable, repeatable demo** over cleverness.

## B2. Operating loop (every iteration)
1. **Read** `AGENTS.md`, `PROGRESS.md`, `docs/decisions/` and the current iteration prompt.
2. **Plan** in ≤15 lines: tasks, files to touch, risks. Write it at the top of the iteration's section in `PROGRESS.md`.
3. **Implement** in small commits (`iter-N: <what>`).
4. **Verify** by running every acceptance command in the Definition of Done. Paste real output (counts, timings), not claims.
5. **Record** decisions in `docs/decisions/NNN-title.md` (context, options, choice, consequences) and the assumptions list in `docs/assumptions.md`.
6. **Update** `PROGRESS.md` (done / not done / blockers / next) and tag `iter-N`.
7. **Stop** and report. Do not start the next iteration.

## B3. Engineering rules (non-negotiable)
1. **Never invent facts about the data.** Profile first; model from what exists. Where the design in Part D disagrees with the actual columns, the data wins and you log an ADR.
2. **Verify versions before pinning.** Check current stable releases of Airflow, dbt-core, dbt-duckdb, DuckDB, Superset, Grafana, Postgres in their official docs at build time, then pin **exact** versions in `requirements/*.txt` and image tags. No `latest`. Use official constraint files for Airflow. Airflow 3.x changed imports (`airflow.sdk`), the API server, and the DAG processor, and SLA support differs from 2.x, so follow the docs for the pinned version.
3. **Idempotent everything.** Re-running a task, DAG, or file load must not duplicate rows. Use `(source_file, file_sha256)` uniqueness, `batch_id` tracking, `MERGE`/delete-insert by batch, and dbt incremental models keyed on natural + batch keys.
4. **History is sacred.** Never truncate Bronze or Gold between refreshes. New data **appends**. The demo must show cumulative counts rising.
5. **Atomic file handoff.** Writers create `*.part` and rename on completion. The watcher ignores `*.part` and waits for size stability.
6. **Config over code.** All paths, DSNs, thresholds, and volumes come from `.env` / `config/*.yaml`. No secrets in git. Provide `.env.example`.
7. **Modular DAGs.** `dags/` holds thin definitions only (TaskFlow or operators, no business logic). Logic lives in `include/<domain>/` as importable, unit-testable Python. One concern per DAG. Group tasks with TaskGroups (`extract`, `validate`, `load`, `transform`, `test`, `publish`). Cross-DAG triggers use Assets/Datasets or `TriggerDagRunOperator`, **not** sleeping sensors where avoidable.
8. **Every layer emits metrics** to Postgres schema `obs` (see B6). If a layer produces no metric row, it is not done.
9. **Fail loudly, log richly.** Retries with backoff on I/O tasks, `on_failure_callback` writes to `obs.dag_events`. Bad rows go to `dq.rejected_rows` with a reason code. They are never silently dropped.
10. **Tests are part of the deliverable.** pytest for generator/ingestion logic, dbt tests for models (`unique`, `not_null`, `relationships`, `accepted_values`, plus custom singular tests), and an end-to-end smoke test (`make smoke`).
11. **One-command ergonomics.** `make up`, `make down`, `make reset` (explicit, destructive, asks for confirmation), `make demo-r1`, `make demo-r2`, `make test`, `make logs`.
12. **Do not run destructive commands** (`docker volume rm`, `rm -rf data/`, `DROP SCHEMA`) unless the iteration prompt says so. `make reset` is the only sanctioned path.
13. **Time is UTC.** The generator uses a **simulated clock** stored in `ctl.sim_clock`; real wall-clock is used only for latency and duration metrics.
14. **Large files out of git.** Base CSVs >50 MB go via Git LFS or a documented download step. Never commit `.duckdb` files or `/data`.

## B4. Docker platform contract

Compose profiles: `core` (postgres, airflow-*, ingest-api, file-watcher), `bi` (superset, redis, grafana), `sim` (24/7 simulator, Phase 4).

| Service | Notes |
|---|---|
| `postgres` | One instance, separate databases: `airflow`, `dwh`, `superset`. Schemas in `dwh`: `bronze`, `ctl`, `obs`, `dq` |
| `airflow-*` | LocalExecutor. Examples disabled. Own image: Airflow + provider packages; **dbt installed in an isolated venv** (`/opt/dbt-venv`) to avoid dependency clashes |
| `ingest-api` | FastAPI + Uvicorn. Endpoints: `POST /v1/ingest/file`, `POST /v1/ingest/stream`, `GET /health`, `GET /v1/batches/{id}` |
| `file-watcher` | Python `watchdog` (fallback to polling). Calls `ingest-api`. Auto-restarts |
| `superset` | Custom image with `duckdb-engine` and `psycopg2`. Dashboards and datasets **provisioned from exported YAML** by an init container |
| `grafana` | Provisioned datasources and dashboards (JSON/YAML in repo) |

Every service needs a **healthcheck**; `depends_on` uses `condition: service_healthy`. Declare named volumes for Postgres and Grafana only. Data is bind-mounted at `./data` → `/data`:

```
/data/landing/{batch,stream}   /data/archive   /data/rejected
/data/warehouse/dwh.duckdb     /data/serving/dwh_serving.duckdb
```

Budget: the whole stack must run on **8 GB RAM**. If it does not, document the minimum and trim (e.g., drop Redis, one Airflow worker process).

## B5. Repo layout

```
.
├── AGENTS.md  PROGRESS.md  Makefile  docker-compose.yml  .env.example
├── dags/                     # thin DAG files only
├── include/
│   ├── generator/            # causal data simulator (Part C-3)
│   ├── ingestion/            # parsers, validators, loaders
│   ├── observability/        # metric writers
│   └── publish/              # serving-snapshot swap, Superset cache bust
├── services/{ingest_api,file_watcher,sim_runner}/
├── dbt/                      # models/{silver,gold,agg,semantic}, snapshots, tests, macros, semantic YAML
├── sql/{ddl,bench}/          # Postgres DDL, benchmark queries (tagged by dashboard+widget)
├── bi/{superset,grafana}/    # exported, provisioned assets
├── data/                     # gitignored
├── excel/                    # per-phase design workbooks
├── reports/  docs/  ppt/  tests/
```

## B6. Observability schema (`dwh.obs`), the backbone of five graded dashboards

| Table | Key columns |
|---|---|
| `batch_load_log` | batch_id, run_id, source_domain, file_name, file_sha256, start_ts, end_ts, **duration_s**, rows_read, **rows_loaded**, rows_rejected, **status**, error_text, attempt |
| `stream_metrics` | window_start, window_end, events_in, events_ok, **malformed_count**, **throughput_eps**, latency_p50_s, latency_p95_s, latency_max_s |
| `storage_snapshot` | captured_at, schema, table, source_domain, **row_count**, **size_mb** (`pg_total_relation_size`), duckdb_file_mb |
| `date_coverage` | captured_at, source_domain, date_column, min_date, max_date, span_days, months_present, months_expected, missing_months |
| `query_log` | ts, query_id, dashboard, widget, engine, **duration_ms**, rows_returned, **status**, error_text, optimized_flag |
| `generation_log` | refresh_no, sim_window_start/end, source_file, rows_generated, parameters_json |
| `dag_events` | dag_id, run_id, task_id, event, ts, duration_s, state (also feeds SLA monitoring) |
| `sla_log` | dag_id, run_id, expected_s, actual_s, breached |

Metric definitions follow the spec: duration = `end_ts - start_ts` per file; rows = `len(df)` after load; success % = successful ÷ attempted × 100; throughput = records ÷ stream seconds; latency = `db_insert_ts - source_row_created_ts`; malformed = counter in the validation `try/except`; query time via a `time.perf_counter()` wrapper; error rate = failed ÷ executed.
**Storage note:** inside Docker use `pg_database_size()` / `pg_total_relation_size()` for sizes. Optionally add a `du`-based check on the volume to honour the spec's `os.path.getsize` wording, and document it.

## B7. Data-quality contract
- **Bronze:** schema-on-read tolerant. All source columns kept as text plus `_batch_id, _source_file, _ingested_at, _row_hash, _line_no`. Row-level parse failures → `dq.rejected_rows`.
- **Silver:** typed, trimmed, deduped (latest by `_ingested_at` per natural key), referential checks. Required rules: `price > 0`, valid dates (and `expiry > manufacture`), non-null keys, non-negative quantities, temperatures within physical plausibility, lineage keys resolvable.
- **Gold:** dbt tests on every key and relationship. Failing **error** tests block `publish_serving`; **warn** tests are logged to `dq.results`.
- The generator **deliberately injects ~0.5-2% defects** (null keys, negative price, bad dates, schema drift in the stream) so validation and the malformed counter show real, non-zero values. Label them in `generation_log`.

## B8. Reporting style
Concise engineering voice. For each iteration end with: **Done · Evidence (commands + outputs) · Assumptions made · Open questions · Next**.

## B9. When to ask vs. decide
Decide and log an ADR when a choice is reversible. Ask the human only when blocked by: missing files, instructor-defined ambiguity (A2 #1-3), credentials, or an irreversible action.

---

# PART C: ITERATION PROMPTS

> Tags: **[MUST]** needed for the milestone · **[SHOULD]** do if time allows · **[COULD]** stretch.

---

## Iteration 0: Discovery, data profiling, state audit *(22 Nov, ~3 h)*

**Objective:** know the data and the current repo state before building anything.

**Tasks**
1. **[MUST]** Audit existing work (repo, Docker files, prior DAGs). List what is reusable. Skip any later task already satisfied, with evidence.
2. **[MUST]** Profile all 7 files (pandas/DuckDB): columns, types, null %, distinct counts, min/max dates, PK uniqueness, **FK coverage across files** (sales → warehouse lot → shipment → manufacturing batch → medicine; IoT → shipment/warehouse/vehicle/device), numeric distributions, seasonality by month, per-SKU volumes. Output `docs/data_profile.md` plus `docs/erd_source.md` (Mermaid).
3. **[MUST]** Identify from the real columns: allowed temp/humidity ranges per medicine, price/cost columns, forecast vs actual fields in hospital demand, expiry fields, carrier/freight columns, planned vs actual delivery dates, vehicle/device identifiers, breach flags.
4. **[MUST]** Draft the **bus matrix** and dimension/fact list (start from Part D, correct it to reality). Output `docs/bus_matrix.md`.
4b. **[MUST]** Read the existing design workbook(s) in `excel/` (tabs `Dim.Tables`, `Fact.Table.*`, `Star.Schema`). **They are the approved design of record.** Reconcile the bus matrix to them (not the other way round), list any column the data cannot support (e.g., payer, promotion, return flag, customer segment), and log gaps as ADRs.
5. **[MUST]** Write `docs/assumptions.md` (seed with A2) and ADR-001 (architecture, per A4).
6. **[SHOULD]** Define the *inventory-management problem* concretely, in measurable terms, using the data (see Part F). Output `docs/problem_statement.md`.

**Definition of Done**
- `docs/data_profile.md` states row counts matching the spec (63 / 561 / 999 / 112,184 / 500,000 / 27,216 / 293,425) or documents the discrepancy.
- Every cross-file FK has a coverage % and orphan count.
- Bus matrix lists each fact table with grain, type, dimensions, and measures with additivity.

---

## Iteration 1: Docker platform foundation *(22 Nov)*

**Objective:** `make up` yields a healthy, empty stack.

**Tasks**
1. **[MUST]** `docker-compose.yml` per B4 with healthchecks and profiles. `.env.example`, `Makefile`.
2. **[MUST]** Postgres init scripts: databases, schemas `bronze/ctl/obs/dq`, DDL for all `obs.*` and `ctl.*` tables (B6), indexes on timestamp columns.
3. **[MUST]** Airflow image (pinned) with isolated dbt venv; a hello-world DAG that proves: DB connection, writing to `obs.dag_events`, running `dbt debug`.
4. **[MUST]** `ingest-api` skeleton with `/health` and DB connectivity.
5. **[SHOULD]** Superset image with `duckdb-engine`; Grafana with a provisioned Postgres datasource.
6. **[SHOULD]** GitHub Actions or `make lint test` running ruff + pytest + `dbt parse`.

**Definition of Done**
- `docker compose up -d` → all services `healthy` (`docker compose ps` shown).
- Airflow UI reachable; hello DAG succeeds; row visible in `obs.dag_events`.
- Superset and Grafana log in; the Grafana datasource test passes.
- `make down && make up` preserves Postgres data.

---

## Iteration 2: Ingestion, Bronze, batch + streaming observability *(22-23 Nov)*

**Objective:** drop a file in `/data/landing/batch` and see it in Bronze with metrics, automatically.

**Tasks**
1. **[MUST]** `file-watcher` → `ingest-api` → loader. Support `.csv` and `.xlsx`. Pattern `NN_<name>__b<batch>.{csv,xlsx}` maps to the Bronze table. Wait for size stability and ignore `*.part`.
2. **[MUST]** Loader: record `start_ts`; read with pandas (chunked for 500k rows); validate row-level; bulk-load with `COPY`; write `rows_read/rows_loaded/rows_rejected`; record `end_ts`; write `obs.batch_load_log`; archive the file to `/data/archive/<batch>/`; write `ctl.batch_manifest`. **Duplicate file hash → skip and log `status='duplicate'`.**
3. **[MUST]** One-time **historical load** of the 7 base files as `batch_id = 0` (same code path).
4. **[MUST]** Stream path: `stream/*.jsonl` micro-batches (or API `POST /v1/ingest/stream`). Each event carries `event_ts` (source creation). The consumer computes latency at commit, counts malformed events in `try/except`, and writes `obs.stream_metrics` per window (e.g., 10 s).
5. **[MUST]** Failure path test: corrupt file → `status='failed'`, error captured, retry policy exercised, then success on retry. This proves the success-rate metric is real.
6. **[MUST]** Grafana dashboards **"Batch Ingestion"** (duration horizontal bar by source file, rows per batch, success-rate stat, recent failures table) and **"Streaming Ingestion"** (throughput line chart over time, latency p50/p95, malformed count).
7. **[SHOULD]** `obs.storage_snapshot` + `obs.date_coverage` collectors, and a Grafana **"Storage"** dashboard (donut by domain, MB, coverage). A DAG `dag_observability_snapshot` runs every 5 min.

**Definition of Done**
- After `make load-base`: row counts per Bronze table equal source rows; `obs.batch_load_log` has 7 `success` rows.
- Dropping a new file produces a Bronze insert within seconds with **no manual step**; re-dropping the same file creates no duplicates.
- Dashboards render real data; the failure-test row is visible.

---

## Iteration 3: Causal data generator + generation DAG *(23 Nov)*

**Objective:** produce believable, referentially consistent new data for **all 7 files**, forward in time, for two refreshes.

**Design (follow this)**
- **Causal simulation, not 7 independent samplers.** Order: *master changes → manufacturing batches → shipments → warehouse snapshots → sales + hospital demand → IoT readings*. Each stage consumes IDs created upstream, so lineage in `05_pharmacy_sales_data` stays complete.
- **Fit to the real data:** per-SKU volume, price, seasonality, regional split, channel mix, lead times, breach rates, forecast error. Use bootstrap + calibrated noise (optionally `scipy.stats` fits). Do not use naive uniform random.
- **Forward time windows (simulated clock):** R1 = Jan-Mar 2026, R2 = Apr-Jun 2026 (adjust to profile). *"Different time periods"* satisfied, and history accumulates.
- **Volumes:** choose per file, e.g. each refresh ≈ 3-8% of that file's base rows, but sized so a refresh cycle (generate → ingest → dbt → publish) finishes in **≤3 minutes** on the demo laptop. Justify each number in the report (preserve distributions; large enough that KPIs visibly move; small enough to demo live). IoT is generated at a higher rate for streaming.
- **Show SCD2 and late data deliberately:** in R2 change some master-data attributes (price, storage range, supplier/status) for a handful of SKUs, add 1-2 new SKUs, and include a few late-arriving facts and one early-arriving fact (unknown dimension member).
- **Inject defects** (B7) at ~0.5-2%, logged.
- **Outputs per refresh:** delta files `NN_<name>__b<k>.csv` (+ optional `.xlsx`), **also appended to the master `data/source/*.csv`** so "each of the 7 source files grows" is literally true.
- **Reproducibility:** seeded RNG (`seed` stored in `generation_log`).

**Tasks**
1. **[MUST]** `include/generator/` modules per stage, plus a `ProfileFit` module that learns parameters from the base data.
2. **[MUST]** Statistical validation: KS-test/quantile comparison (base vs synthetic) for key numeric columns; FK integrity = 100%; seasonality check. Output `reports/generation_validation.md`.
3. **[MUST]** DAG `dag_generate_data` (params: `refresh_no`, `seed`; tasks `plan → generate_<stage> → validate → write_atomic → log`). A manual-trigger DAG, not scheduled.
4. **[MUST]** Generator CLI parity: `python -m generator --refresh 1`.
5. **[MUST]** `reports/data_generation_report.pdf` (1-2 pages): methodology, why these volumes, per-file row counts, date ranges, injected defect rates, validation results.
6. **[COULD]** Streaming producer mode (events/sec configurable) for Iteration 8 and the Phase 4 simulator.

**Definition of Done**
- `generation_log` rows for all 7 files × R1 and R2.
- 0 orphan FKs in generated data (excluding deliberate early-arriving cases, which are enumerated).
- Running the generator twice with the same seed yields identical files (hash match).
- PDF report ≤2 pages with real numbers.

---

## Iteration 4: Silver + Gold for Phase 1, the Sales & Demand Intelligence mart *(23-24 Nov)*

**Scope (from the Phase 1 workbook):** a **fact constellation of three facts**: `Fact.Table.PharmSales`, `Fact.Table.Inventory`, `Fact.Table.Demand`. Sources: `01_master`, `05_sales`, `06_hospital_demand`, plus **`04_warehouse`** (and `02`/`03` only for batch/lot attributes needed by the inventory fact). The Inventory fact built here is the **first version** of the table Phase 2 extends. Build it once, conformed, and never fork it.

**The three required queries are the acceptance tests of this mart.** Each must exist as a tagged SQL in `sql/bench/`, run correctly on the constellation, and back one dashboard page:

| # | Query (from workbook) | What it forces in the model |
|---|---|---|
| Q1 | Per **month × medicine × disease × region**: pharmacy/e-commerce units sold vs hospital **requested, received, consumed, unfulfilled** | **Drill-across** between `PharmSales` (transaction, daily) and `Demand` (monthly periodic snapshot) at the conformed grain *month × medicine × disease × region*. Aggregate each fact separately, then join. Needs conformed `dim_date` (month level), `dim_medicine` (with disease/indication), `dim_region`. Confirm from data how hospital-channel sales are treated so hospital volume is not double-counted against hospital demand |
| Q2 | For medicines with high hospital demand or high sales: which **warehouses and batch/lots** show stockout exposure, low available qty, near-expiry risk, expired qty, weak FEFO compliance | `Inventory` fact (lot × warehouse × day, semi-additive) joined to Q1's demand/sales ranking; `dim_warehouse`, `dim_batch/lot`, role-playing expiry date; metrics: available qty, stockout exposure, near-expiry bucket, expired qty, FEFO compliance % |
| Q3 | How **net sales, gross margin, return rate, days-to-expiry-at-sale** vary by **channel, customer segment, payer, promotion** | Dimensions `dim_channel`, `dim_customer_segment`, `dim_payer`, `dim_promotion` (or one **junk dimension** if low-cardinality); measures net sales, COGS/margin, returns (qty and value), and `days_to_expiry_at_sale` derived via the sale → lot lineage (expiry date minus sale date). Return rate = returned units ÷ sold units, never an average of ratios |

**Tasks**
1. **[MUST]** dbt-duckdb project. Sources read from Postgres via `ATTACH`. Silver models (`stg_*` → `silver_*`) apply the Phase 1 rules: `price > 0`, valid dates, non-null SKU IDs. Rejections land in `dq.rejected_rows`.
2. **[MUST]** Gold models (see Part D): `dim_date` (+ role-playing views), `dim_medicine` as **SCD Type 2** via dbt snapshot with point-in-time fact lookups, `dim_channel`, `dim_hospital`, `dim_region`, a **junk dimension** for low-cardinality flags, and an unknown member (`-1`) in every dim.
3. **[MUST]** Facts (names mirror the workbook tabs): `fact_pharm_sales` (transaction grain), `fact_inventory` (periodic snapshot, daily lot level, semi-additive), `fact_demand` (hospital × medicine × month, periodic snapshot; requested / received / consumed / unfulfilled / forecast). Incremental by `_batch_id`. Optionally `fact_returns` if returns are separate events in the data.
4. **[MUST]** Airflow `dag_mart_sdi`: `wait/check manifest → dbt build silver → dbt build gold → dbt test → publish_serving → write obs`. Triggered by the ingestion Asset/manifest, not a clock.
5. **[MUST]** Query models `q1_sales_vs_hospital_demand`, `q2_stockout_expiry_exposure`, `q3_commercial_profitability`, plus supporting KPIs: forecast-vs-actual ratio, unfulfilled demand, channel revenue and gross margin, fast/slow-mover rank by therapeutic class (velocity definition documented).
6. **[SHOULD]** Seed the **metric dictionary** (`docs/metrics.md`, MetricFlow YAML draft) with the Phase 1 metrics now.
7. **[MUST]** Keep `excel/DAWH_DWH_Pharma_ColdChain_Sales_Demand-NN.xlsx` **in sync with the dbt models**: every dim/fact column in the workbook exists in Gold with the same name and type, and each of the 3 queries includes its SQL and a result screenshot as the "prove it" evidence. Add a CI check that diffs workbook columns against `information_schema`.

**Definition of Done**
- `dbt build` green; all key/relationship tests pass. Fact row counts reconcile to Silver, and Silver reconciles to Bronze minus rejects (**reconciliation query in `tests/`**).
- **Q1, Q2 and Q3 each run on the Gold constellation**, return non-empty results, and reconcile: Q1 units sold equals `SUM(fact_pharm_sales)` for the same filters, and Q1 hospital quantities equal `SUM(fact_demand)` (no fan-out or double counting).
- Workbook-vs-Gold column check passes.
- After R1 load: `dim_medicine` shows ≥1 SKU with two versions (SCD2 proof) and facts point to the correct version by date.
- Running the DAG twice with no new data changes **nothing** (idempotency).

---

## Iteration 5: Analytical query layer + optimization *(24 Nov)*

**Tasks**
1. **[MUST]** `sql/bench/` holds the **canonical dashboard queries**, each tagged `-- dashboard: X; widget: Y`. These exact queries power the Superset datasets *and* the benchmark.
2. **[MUST]** Benchmark harness: `time.perf_counter()` wrapper, run N times, log to `obs.query_log` with `status`/`error_text`. A DAG task `run_query_benchmark` runs after every publish.
3. **[MUST]** Optimization, **measured before/after** (`EXPLAIN ANALYZE` plans saved to `docs/query_optimization.md`):
   - pre-aggregated `agg_*` tables (DuckDB has no materialized views, so build summaries in dbt and refresh incrementally),
   - sort/cluster fact tables by date on insert (zone-map pruning), Hive-partitioned Parquet export for the snapshot fact (partition by `snapshot_date`) where it helps,
   - ART indexes only for point-lookups; Postgres staging indexes/partitions where queried,
   - join-order and pushdown fixes on the worst two queries.
4. **[MUST]** Grafana **"Query Performance"** dashboard: avg execution time per widget (column chart), daily query count, error rate, p95, and *before vs after optimization*.
5. **[SHOULD]** Pull the real daily query count from Superset's metadata `logs` table too, and show both.
6. **[COULD]** A clearly labelled "chaos" toggle that fires one malformed query to show error-rate capture.

**Definition of Done:** the two slowest queries show a documented speed-up; **all Phase 1 widget queries <1 s** at current volumes (state the volumes); `obs.query_log` has ≥50 rows across ≥8 widgets.

---

## Iteration 6: Phase 1 BI + two live refreshes *(24-25 Nov) → MILESTONE 2*

**Tasks**
1. **[MUST]** Superset: datasets on `sem_*`/Gold views from the **serving snapshot** (read-only). Dashboards:
   - **Q1 page:** *Sales vs Hospital Demand* (units sold vs requested/received/consumed, **unfulfilled demand** hotspots by disease and region, forecast vs actual)
   - **Q2 page:** *Stockout and Expiry Exposure for High-Demand Medicines* (warehouse and lot drill-down, near-expiry, expired qty, FEFO %)
   - **Q3 page:** *Commercial Profitability* (net sales, gross margin, return rate, days-to-expiry-at-sale by channel, segment, payer, promotion; Retail / Hospital / E-commerce split)
   - **Supporting page:** *Top-10 Fast vs Slow movers by Therapeutic Class*
   Each has KPI cards, filters (date, region, class, SKU), a story headline, and a **"data as of / last refresh #"** card.
2. **[MUST]** Dashboard auto-refresh (e.g., 10-30 s) and low/zero cache TTL for the demo. `publish_serving` also busts the Superset cache (API call).
3. **[MUST]** Export dashboards as code into `bi/superset/` and make `make up` re-import them.
4. **[MUST]** Run **Refresh 1** then **Refresh 2** end to end: generate → watcher ingests → Airflow marts → publish → dashboards change. Capture **before/after screenshots and KPI deltas** in `docs/refresh_evidence/`.
5. **[MUST]** Rehearsal script `docs/demo_p1.md` (≤8 min).
6. **[SHOULD]** Draft report sections: assumptions + the story of each dashboard.

**Definition of Done:** a cold `make reset && make up && make load-base && make demo-r1 && make demo-r2` reproduces the full demo with no manual steps; the dashboard KPI values differ between base, R1, and R2, and the deltas are explained.

---

## Iteration 7: Phase 2, Inventory, Expiry & Replenishment mart *(26 Nov → 5 Dec)*

**Sources:** `02_manufacturing`, `03_manufacturer_delivery`, `04_warehouse` (+ conformed `dim_medicine`).

**Tasks**
0. **[MUST]** **Extend, do not rebuild,** the `fact_inventory` and `dim_warehouse` created in Phase 1 (add manufacturing and shipment lineage, FEFO logic depth, replenishment metrics). Update the Phase 1 workbook tabs where columns change, and create the Phase 2 workbook in the same layout.
1. **[MUST]** Silver/Gold: `dim_warehouse` (SCD2 on capacity/status if the data supports it), `dim_manufacturer_plant`, `dim_batch`, role-playing `dim_date` (manufacture / expiry / ship / delivery / snapshot). Facts: `fact_inventory_snapshot` (**periodic snapshot, daily, lot level; semi-additive**), `fact_shipment_line` (transaction), `fact_manufacturing_batch` (accumulating snapshot if lifecycle dates exist).
2. **[MUST]** Metrics: **Stockout Risk**, **FEFO Compliance %**, **Days Remaining Shelf Life**, days-of-cover, overstock flag vs threshold, near-expiry buckets (30/60/90) with **financial at-risk value**. Definitions in `docs/metrics.md` with additivity notes.
3. **[MUST]** Partition snapshot facts by `snapshot_date`; daily snapshot extraction automated in `dag_mart_irm` (`@daily`-style plus manual trigger; the demo uses the trigger).
4. **[MUST]** Dashboards: *Regional Warehouse Stockout vs Overstock Monitor*, *Near-Expiry Risk Matrix (30/60/90 + ₨/$ at risk)*, *FEFO Compliance per Warehouse*.
5. **[MUST]** Two refreshes demonstrated (R1/R2 data already exist from Iteration 3 for these files).
6. **[MUST]** Extend query benchmark and storage dashboards to the new marts; `excel/phase2_design.xlsx`.
7. **[SHOULD]** Conformed-dimension reuse proof: `dim_medicine` is the *same* table in the SDI and IRM marts, with a test asserting key equality.

**Definition of Done:** FEFO compliance reproducible by an independent SQL check on a sample warehouse-day; near-expiry value reconciles to snapshot × cost; semi-additive measures are never summed across time in any dataset.

---

## Iteration 8: Phase 3, Traceability & IoT Cold-Chain mart *(6 → 14 Dec)*

**Sources:** `03`, `04`, `07` (+ `dim_medicine`, **`dim_vehicle`, `dim_device`**).

**Tasks**
1. **[MUST]** Micro-batch DAG `dag_stream_iot` (every 1-5 min, `max_active_runs=1`, `catchup=False`) consuming `stream/` and writing Bronze → Silver incrementally. The streaming dashboard from Iteration 2 shows it live.
2. **[MUST]** Dynamic range validation: join each reading to the medicines in that shipment/storage zone through a **bridge table** (`bridge_shipment_medicine`) and flag breaches against **each medicine's allowed limits**. Excursion events go to a factless/event fact.
3. **[MUST]** Facts: `fact_iot_reading` (transaction), `fact_thermal_exposure_hourly` (periodic aggregate: minutes out of range, max deviation, **mean kinetic temperature (MKT)**, shock count), `fact_excursion_event`, `fact_delivery` (accumulating snapshot: planned vs actual → OTIF).
4. **[MUST]** Traceability queries: forward and backward trace for any lot (manufacturing batch → shipment → warehouse → sale) plus recall-scope report. Add a lineage dashboard page.
5. **[MUST]** Dashboards: *Live Temperature/Humidity Excursion Heatmap (warehouse zones and in-transit vehicles)*, *Carrier OTIF and Freight-Cost Efficiency*, *Batch Traceability and Quarantine*.
6. **[MUST]** Two refreshes (micro-batch runs + bulk R1/R2); `excel/phase3_design.xlsx`.
7. **[SHOULD]** Alert table `gold.alert_excursion` + Grafana alert rule. **[COULD]** Redpanda as the stream transport.

**Definition of Done:** an injected excursion is detected within one micro-batch cycle and appears on the heatmap; OTIF and freight efficiency reconcile with a hand-computed sample; the latency metric is non-trivial and plausible.

---

## Iteration 9: Fact constellation, semantic layer, inventory solution *(Bonus)*

**Tasks**
1. **[MUST]** Integrate the three marts into **one Gold constellation** over **conformed dimensions** (`dim_date`, `dim_medicine`, `dim_warehouse`, `dim_region`, `dim_vehicle`, …). Create **drill-across** models (per-fact aggregates at conformed grain, then joined, to avoid fan-out and double counting).
2. **[MUST]** **Semantic layer** per Part E.
3. **[MUST]** **Inventory-management solution** per Part F: `fact_inventory_health_daily`, `mart_replenishment_recommendation`, policy backtest.
4. **[MUST]** Master DAG `dag_enterprise_master`: orchestrates generate → ingest sensors → three mart DAGs (Assets) → constellation build → semantic tests → publish → benchmark → observability. **Cross-mart dependency sensors**, retry policies with exponential backoff, **SLA monitoring** (see B3.2 note on version differences: implement via `obs.sla_log` + callbacks if native SLA isn't available).
5. **[MUST]** Optimize multi-fact queries (evidence in `docs/query_optimization.md`).
6. **[MUST]** **Enterprise 360° Inventory Intelligence dashboard** (Superset): supply (production, in-transit), stock (cover, overstock, expiry), demand (sales, hospital forecast), cold-chain risk (excursions, quarantined value), plus a **Recommendations** page (what to reorder, move, or discount today).
7. **[MUST]** Run the constellation's **two refreshes** (R3/R4 generated as new windows, or reuse R1/R2 with fresh simulation windows; state which).
8. **[SHOULD]** 24/7 multi-threaded simulator container (`sim` profile): threads for manufacturing releases, shipments, warehouse snapshots, sales, IoT streaming, with rate configs and a kill switch.
9. **[COULD]** Cube.dev on top of `sem_*` as an alternative semantic server.

**Definition of Done:** one query joins sales, inventory, and excursions through conformed dims with **correct, reconciled** totals (test: constellation totals = sum of the individual mart totals at the same grain); the recommendation backtest shows a quantified improvement over the baseline (Part F).

---

## Iteration 10: Hardening, unified observability, report, demo

**Tasks**
1. **[MUST]** **Unified DE Observability dashboard** (Grafana): DAG success/duration/SLA, ingestion (batch + stream), storage, query performance, DQ results, freshness by mart.
2. **[MUST]** Failure drills: kill the watcher; corrupt a file; stop Postgres briefly. Show recovery and the retries in the dashboard.
3. **[MUST]** Final **project report** (Part G) and **PPT**. `README.md` with a 5-command quickstart and a demo link.
4. **[MUST]** Clean-clone test on a fresh machine or directory: `git clone` → `make up` → full demo works.
5. **[MUST]** Final demo script (≤12 min) with a timed checklist and a **backup screen recording**.
6. **[SHOULD]** Tag `v1.0`, and publish large data via LFS or a release asset.

---

# PART D: DIMENSIONAL DESIGN STARTING POINT (validate with profiling)

**Bus matrix** (● = used). Final column names come from the real data.

| Fact (grain, type) | Date | Medicine | Warehouse/Region | Hospital | Channel | Plant | Carrier | Vehicle | Device | Batch | Junk flags |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `fact_sales` (1 transaction, transaction) | ● | ● | ● |  | ● |  |  |  |  | ● | ● |
| `fact_hospital_demand` (hospital×medicine×month, periodic snapshot) | ● | ● | ● | ● |  |  |  |  |  |  |  |
| `fact_manufacturing_batch` (1 order, accumulating snapshot) | ● | ● |  |  |  | ● |  |  |  | ● | ● |
| `fact_shipment_line` (shipment+line, transaction) | ● | ● | ● |  |  | ● | ● | ● |  | ● |  |
| `fact_inventory_snapshot` (lot×warehouse×day, periodic, semi-additive) | ● | ● | ● |  |  |  |  |  |  | ● | ● |
| `fact_delivery` (1 shipment, accumulating: ship→ETA→delivered) | ● |  | ● |  |  | ● | ● | ● |  |  | ● |
| `fact_iot_reading` (1 reading, transaction) | ● | via bridge | ● |  |  |  |  | ● | ● |  | ● |
| `fact_thermal_exposure_hourly` (zone/vehicle×hour, periodic aggregate) | ● | via bridge | ● |  |  |  |  | ● | ● |  |  |
| `fact_excursion_event` (excursion×affected lot, **factless/event**) | ● | ● | ● |  |  |  |  | ● | ● | ● |  |
| `fact_inventory_health_daily` (SKU×warehouse×day, derived snapshot) | ● | ● | ● |  |  |  |  |  |  |  |  |

**Dimension techniques to demonstrate (each at least once, named in the report):**
- **SCD Type 2:** `dim_medicine` (price, storage range, status), optionally `dim_warehouse`. Type 1 for corrections. Type 0 for natural keys and original dates.
- **Role-playing:** `dim_date` as manufacture / expiry / ship / delivery / sale / snapshot date views.
- **Junk dimensions:** `dim_sales_profile` (payment type, prescription flag, discount flag…), `dim_iot_flags` (breach, shock, door-open…), built from actual low-cardinality columns.
- **Degenerate dimensions:** shipment ID, transaction ID, order ID.
- **Bridge:** shipment ↔ medicine (many-to-many for IoT-to-medicine mapping).
- **Fact types:** transaction, periodic snapshot, accumulating snapshot, factless, aggregate.
- **Hygiene:** unknown/inferred members (-1), late-arriving-fact handling, surrogate keys (stable hash or integer), conformed dimensions with identical keys across marts.

---

# PART E: SEMANTIC LAYER SPECIFICATION

1. **Gold → `sem_*` views:** business-friendly names, one view per business entity/process (`sem_sales`, `sem_inventory`, `sem_shipments`, `sem_cold_chain`, `sem_replenishment`), denormalised with conformed dims, no technical keys exposed, and role-playing dates renamed clearly.
2. **Governed metrics** in dbt **MetricFlow** YAML (`semantic_models`, `metrics`). Verify MetricFlow + the DuckDB adapter work in the pinned stack. If not, fall back to SQL metric views plus a YAML dictionary, and log an ADR. Required metrics:

| Domain | Metrics |
|---|---|
| Sales/demand | revenue, gross margin %, units sold, forecast accuracy (WAPE), fill rate, unfulfilled demand rate |
| Inventory | on-hand units/value, days of cover, stockout risk index, overstock ratio, FEFO compliance %, days remaining shelf life, near-expiry value at risk (30/60/90), inventory turnover, waste/expiry-loss rate |
| Cold chain | excursion rate, thermal exposure minutes, MKT, quarantined value, % lots with excursion |
| Logistics | OTIF %, lead time, freight cost per unit |
| Composite | Inventory Health Score (0-100, weights documented) |

3. **Additivity rules baked in:** ratios are always `sum(numerator)/sum(denominator)` (never averages of ratios); balances (stock) are **semi-additive** (last or average over time, summed across warehouses); price/temperature are non-additive.
4. **Metric dictionary** `docs/metrics.md` (auto-generated from YAML): name, business definition, formula, grain, additivity, owner, source tables, caveats.
5. **BI contract:** Superset datasets reference **only** `sem_*` (or certified metrics). No dashboard-local SQL logic for KPIs. Dashboard widgets are tagged for the query benchmark.
6. **Tests:** every metric has a reconciliation test against a hand-written SQL on a sample.

---

# PART F: SOLVING THE INVENTORY-MANAGEMENT PROBLEM

**Problem statement (refine in Iteration 0):** *Cold-chain medicines are simultaneously at risk of stockout (lost sales/unfulfilled hospital demand) and overstock/expiry (waste), and stock is silently lost to temperature excursions. Decisions are made without a joint view of supply, demand, shelf life, and cold-chain integrity.*

**Solution = measurable diagnosis + transparent decision layer + backtest** (no black-box ML):

1. **Available-to-promise stock:** on-hand minus quarantined (excursion-affected lots) minus lots whose remaining shelf life < a minimum-sellable threshold.
2. **Demand signal:** blend of recent sales velocity and hospital forecast, with **forecast error** (from `fact_hospital_demand`) used for safety stock. A seasonal-naive or ETS baseline is allowed.
3. **Policy per SKU×warehouse:** lead time (from shipments: mean and σ) → **safety stock** (`z·σ_d·√L`), **reorder point**, **target cover**, and **max stock cap** limited by shelf life (do not order more than can be sold before expiry).
4. **Recommendations (`mart_replenishment_recommendation`):** reorder qty, *transfer* surplus between warehouses, *expedite/discount* near-expiry lots, *prioritise* FEFO picks, and *hold/investigate* excursion lots, each with a reason code and **₨/$ impact**.
5. **Backtest** over the history: baseline (observed behaviour) vs policy → stockout days, unfulfilled units, expiry-waste value, avg inventory value, excursion exposure. Report improvement honestly, including limitations.
6. **Dashboard page:** "What to do today", with the top actions ranked by value, drillable to lot-level traceability.

---

# PART G: DEMO AND REPORT CHECKLIST

**Live-demo rules (grading criterion 3: "dashboards must visibly change")**
- Start from a state with base + R1 loaded; open Superset/Grafana/Airflow in three windows. Trigger R2 and narrate: *generation → watcher ingest (Grafana batch dashboard) → mart DAG (Airflow graph) → publish → Superset auto-refresh shows new numbers → "last refresh #" card increments*.
- Pre-write the expected KPI deltas on a cheat sheet. Have a backup recording and a pre-warmed state.
- Keep each refresh cycle ≤3 minutes. Never demo on first-time image builds.

**Report must contain** (grading criterion 4): all assumptions (A2 + `docs/assumptions.md`); architecture and ADR summary; data-generation methodology; DQ rules and injected-defect results; dimensional models with ERDs; SCD/junk/role-playing/fact-type explanations; query-optimization evidence; **each dashboard: purpose, KPIs, definition, and the story it tells with before/after refresh numbers**; inventory-problem solution and backtest; limitations and future work.

**GitHub:** code, Excel workbooks, PPTs, report, `README`, demo link, `docs/`. Private until approved. No secrets or large binaries.

---

# APPENDIX: Prompt template to launch an iteration

```
You are working in the repo at <path>. First read AGENTS.md, PROGRESS.md and docs/decisions/.
Today's task: ITERATION <N> from AGENT_INSTRUCTIONS (paste the iteration section below).
Constraints: follow the operating loop in B2; tag priorities [MUST]/[SHOULD]/[COULD]; if time is short, drop COULD then SHOULD.
Current situation: <what's already done, what's broken, hours available>.
Finish with: Done · Evidence · Assumptions · Open questions · Next. Do not start the next iteration.

<paste iteration section>
```
