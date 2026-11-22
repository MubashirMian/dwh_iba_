# AGENTS.md: SDI Mart (Pharma Cold-Chain DWH), Source → Bronze → Silver → Gold → Query Layer

**Version 1.0 · written 22 Nov 2026 · Master's course: Data Warehousing & Analytics**
**Scope of this file:** everything up to and including the **query layer** of the Phase 1 "Sales & Demand Intelligence (SDI)" mart. Dashboards (Superset), the data generator, the two refreshes, Phases 2/3 and the semantic layer are **out of scope** here (see Section 12).
**Deadline pressure:** Phase 1 Milestone 2 is **Wed 25 Nov 2026**. Items are tagged **[MUST] / [SHOULD] / [COULD]**. If time runs short, drop COULD, then SHOULD. Never drop MUST.

> Save this file as `AGENTS.md` in the repo root. The agent reads it at the start of **every** session, together with `PROGRESS.md`.

---

## 0. THE FIVE RULES THAT OVERRIDE EVERYTHING

1. **Everything runs in Docker.** The only thing assumed on the host is Docker + Docker Compose (+ git). No `pip install`, no host Python, no host Postgres. Every script, verification, dbt command and test runs via `docker compose run --rm tools ...` or inside the Airflow container. If Docker is not usable from your environment, **STOP and tell the human**. Do not fall back to host installs, DuckDB-as-Bronze, or CSV-only shortcuts.
2. **`PROGRESS.md` is your memory, not the chat.** The human may run out of account/context limit at any moment and hand the repo to a different AI agent. That agent knows **only** what is in the repo. Follow the handoff protocol in Section 2 exactly, after **every step**, not only at the end of a stage.
3. **The data is the source of truth.** The Excel design workbook is a set of hypotheses to test. Never invent columns, values or rules. If something is untested, write `NOT TESTED` and why.
4. **Source files and workbook `-00` are immutable.** Never modify, move or delete them. Record SHA-256 checksums at the start and prove they are unchanged at the end.
5. **No claim without evidence.** Every "done" is backed by a command you ran and its real output (counts, timings), saved to a file under `docs/`. No fabricated numbers, no hard-coded dashboard values.

---

## 1. TARGET ARCHITECTURE (decided; do not re-litigate)

```
Source Excel/CSV files (read-only mount)
   → Python loader  (include/ingestion + scripts/load_bronze.py)   [run by Airflow]
   → BRONZE   PostgreSQL schema `bronze`  (raw text + technical columns + bronze.load_manifest)
   → SILVER   dbt-postgres → schema `silver`  (typed, trimmed, deduped; rejects → dq.rejected_rows)
   → GOLD     dbt-postgres → schema `gold`    (dims, facts, agg_* tables)
   → QUERY LAYER  sql/bench/*.sql (tagged canonical queries) + benchmark harness + optimization + obs.query_log
   → (later, out of scope) semantic layer sem_* → Superset dashboards

Airflow (`dag_mart_sdi`) ORCHESTRATES the steps; it does not move data itself.
Prometheus + Pushgateway + Grafana show real ingestion metrics.
Grafana (Postgres datasource) shows the Query Performance dashboard from obs.query_log.
```

**Resolved conflicts between the two original instruction files** (log each as an ADR in Stage 0):

| Topic | Decision |
|---|---|
| dbt adapter / marts engine | **dbt-postgres**, Silver and Gold in PostgreSQL. **Not** dbt-duckdb. (The newer, more specific sub-instruction overrides the older DuckDB design.) |
| DuckDB | **Verification only** (Stage 1 scratch analysis). Never Bronze, never the dbt target, no "serving snapshot" swap. |
| Ingestion trigger | **Airflow runs the Python loader directly** (task `load_excel_to_postgres_bronze`). No file-watcher / FastAPI service in this scope. |
| Ingestion metrics | **Prometheus + Pushgateway → Grafana** (metric names in Section 9). |
| Query-layer metrics | **Postgres table `obs.query_log`** read by a Grafana **Postgres** datasource (so Grafana has two datasources: Prometheus + Postgres). |
| Source format | Inspect the **actual** files. Support `.xlsx/.xls` (openpyxl) and `.csv`. Prompt-A style discovery may use CSVs; production loader supports whatever is really supplied. |
| Time / SCD2 history | Base data may have no SCD2 history. If so, see Stage 6, step S6.5 (controlled test fixture; the full generator + R1/R2 refreshes come in a later iteration). |

---

## 2. HANDOFF PROTOCOL (the most important operational rule)

### 2.1 Files you must create and keep current

| File | Purpose |
|---|---|
| `PROGRESS.md` | **Single source of truth for resuming.** Format in 2.3. Updated constantly. |
| `docs/decisions/NNN-title.md` | One ADR per decision (Section 10). |
| `docs/assumptions.md` | Running list of assumptions. |
| `docs/commands.md` | Exact commands to start, stop, run each stage, and run each check. A new agent must be able to resume from this file alone. |
| Git commits | One commit **per step**: `S<stage>.<step>: <what>`. Initialize git if absent. Commit `PROGRESS.md` with every step. Never commit `.env`, data files, `.duckdb` files. |

### 2.2 When to update `PROGRESS.md`
1. **Before** starting a step: set its status to `IN PROGRESS` and write a ≤10-line plan.
2. **After any long or risky command** (builds, loads, dbt runs): one line of what ran and the result.
3. **After** finishing a step: status `DONE` + evidence file path + key numbers; update **"RESUME HERE"** block (2.3).
4. **Whenever you hit a blocker or make a non-obvious choice.**
5. If you sense you are running low on context/limit: immediately write a complete "RESUME HERE" block and commit. Do this *before* starting anything big.

**Context hygiene (saves your limit):** write large outputs to files under `docs/` and `sql/.../results/`; paste only summaries and key numbers into chat. Do not re-print big tables. Do not re-read files you already summarized in `PROGRESS.md`.

### 2.3 `PROGRESS.md` template (create in S0.3)

```markdown
# PROGRESS: SDI Mart
Last updated: <UTC timestamp> by <agent/session label>

## RESUME HERE (always accurate; rewrite after every step)
- Current stage/step: S<x>.<y> <name>   Status: IN PROGRESS | BLOCKED | DONE
- What was last done (1-3 lines):
- Exact next action (a command or file to open):
- Environment state: containers up? (`docker compose ps` summary), which DB schemas exist, last Airflow run id/state
- Known failures / things that are half-done and must not be assumed to work:
- Open human questions (with my recommendation):

## STEP CHECKLIST
| Step | Title | Tag | Status | Evidence file | Commit |
|---|---|---|---|---|---|
| S0.1 | ... | MUST | TODO | | |
(all steps from this AGENTS.md, copied in S0.3)

## STAGE LOG (append-only, newest at bottom)
### S<x>.<y>: <title>
- Plan:
- Commands run + result (real numbers):
- Decisions/ADRs:
- Assumptions:
- Evidence files:

## DECISIONS INDEX (ADR number: title: one-line outcome)
## ASSUMPTIONS INDEX
## KNOWN RISKS TO 25 NOV
```

### 2.4 Starting a session (every session, including a brand-new agent)
1. Read `AGENTS.md`, then `PROGRESS.md` (especially **RESUME HERE**), then `docs/decisions/` titles and `docs/commands.md`.
2. Run `docker compose ps` to learn the real state; reconcile it with `PROGRESS.md`. Trust the **running state and files**, and fix `PROGRESS.md` if they disagree.
3. Continue from "Exact next action". Do **not** redo `DONE` steps unless their evidence file is missing or a check fails.

### 2.5 Mode of operation
Work continuously through the stages in order. Stop only for: (a) a true blocker (missing file, Docker unusable, credentials), (b) an instructor-defined ambiguity, (c) an irreversible action, or (d) completion of Stage 10. For reversible choices, decide, log an ADR, and flag it `ASSUMED, human may review` in `PROGRESS.md`. At the end of **each stage**, write a short report: **Done · Evidence · Assumptions · Open questions · Risks to 25 Nov · Next**.

---

## 3. ENGINEERING RULES (non-negotiable)

1. **Pin versions. Never `latest`.** At build time check current stable releases from official sources (docs / PyPI / registries) for Airflow, dbt-core, dbt-postgres, PostgreSQL, Prometheus, Pushgateway, Grafana, Python base image. Pin exact versions in `requirements/*.txt` and image tags, mutually compatible. Use Airflow's official constraint file. Record versions in an ADR. If you cannot verify online, say so and record the source of your choice.
2. **Idempotent everything.** Re-running a task, DAG, loader or dbt build must not duplicate rows or change results when no new data exists.
3. **No secrets in git.** `.env` is git-ignored; ship `.env.example`; compose and `profiles.yml` read from environment.
4. **Config over code.** Paths, DSNs, thresholds in `.env` / `config/*.yaml`.
5. **Thin DAGs.** DAG files only wire tasks. Logic lives in `include/<domain>/` as importable, testable Python (pytest).
6. **Fail loudly.** Retries + delays on I/O tasks, timeouts, clear logs. A failed Bronze load or validation must **block** all downstream dbt tasks. The loader exits non-zero on any failed required input. Never silently skip, never silently drop rows. Rejected rows go to a documented rejects table with reason codes.
7. **Do not run destructive commands** (`docker volume rm`, `DROP SCHEMA ... CASCADE`, `rm -rf data/`) unless a step says so. Provide `make reset` (asks confirmation) as the only sanctioned destructive path.
8. **Docker hygiene:** health checks on every service, `depends_on: condition: service_healthy`, restart policies, named volumes for Postgres/Prometheus/Grafana, a dedicated network, no source data baked into images (mount read-only), stack must fit in **8 GB RAM** (document minimums if not).
9. **Makefile ergonomics:** `make up`, `make down`, `make reset`, `make tools` (shell in tools container), `make verify`, `make load-base`, `make dbt-build`, `make test`, `make bench`, `make logs`.
10. **UTC everywhere.**
11. **Large files out of git** (data, `.duckdb`, outputs of loads).

---

## 4. REPO LAYOUT (create in S0.2)

```
.
├── AGENTS.md  PROGRESS.md  README.md  Makefile  docker-compose.yml  .env.example  .gitignore
├── docker/                    # Dockerfiles: tools/, airflow/
├── dags/                      # dag_mart_sdi.py (thin)
├── include/{ingestion,observability,bench}/    # importable logic
├── scripts/                   # verify_sdi.py, load_bronze.py, check_bronze.py, run_bench.py
├── dbt/                       # dbt project (models/{silver,gold,agg}, snapshots, tests, macros)
├── sql/{verification,bench,ddl}/   # + sql/verification/results/*.csv
├── config/                    # prometheus.yml, grafana provisioning (datasources + dashboards JSON)
├── excel/                     # workbook -00 (original, immutable) and -01 (new)
├── data/                      # GITIGNORED. data/source (read-only mount), data/scratch
├── docs/{sdi_verification,bronze,decisions,refresh_evidence}/  docs/{assumptions.md,commands.md,query_optimization.md,metrics.md}
├── tests/
└── requirements/
```

---

## 5. STAGE 0: Bootstrap and handoff scaffolding (~1 h)

| Step | Task | Tag |
|---|---|---|
| S0.1 | Locate inputs: the **source files** (01_master, 02_manufacturing, 03_manufacturer_delivery, 04_warehouse, 05_pharmacy_sales, 06_hospital_demand) and the **workbook** (`DAWH_DWH_Pharma_ColdChain_Sales_Demand-00.xlsx` or similar). If any is missing, **STOP and ask**. Compute and store SHA-256 checksums in `docs/bronze/source_checksums.txt`. | MUST |
| S0.2 | Create repo layout (Section 4), `git init`, `.gitignore`, `.env.example`, `Makefile` skeleton. Source files are placed/mounted under `data/source/` (copy only if the human provides them elsewhere; never alter originals). | MUST |
| S0.3 | Create `PROGRESS.md` (template 2.3, with the full step checklist copied from this file), `docs/commands.md`, `docs/assumptions.md`. Save a copy of this file as `AGENTS.md` if not already there. | MUST |
| S0.4 | Check Docker + Compose work. Build the **`tools` image** (Python + pandas, openpyxl, duckdb, psycopg, matplotlib, pytest, pyyaml; for verification only for DuckDB). Prove it: `docker compose run --rm tools python -c "import duckdb,pandas,openpyxl; print('ok')"` with `./data/source` mounted **read-only** and `./docs`, `./sql`, `./scripts`, `./data/scratch` writable. | MUST |
| S0.5 | ADR-001: architecture (Section 1 table, including conflict resolutions). ADR-002: pinned versions list (can be completed in S3.1). | MUST |

**DoD:** `docker compose run --rm tools ...` works; checksums recorded; `PROGRESS.md` exists with a filled RESUME HERE block; first git commit made.

---

## 6. STAGE 1: Design verification against the real data (Prompt A, ~3 h)

**Role:** senior data engineer and Kimball-trained dimensional modeler. **Goal:** verify the workbook's design against the real data. This stage does not build the pipeline. DuckDB here is an ad hoc SQL engine over the source files in the `tools` container. It is **not** a Bronze layer and must never be described as one.

Context: Phase 1 is a fact constellation of three facts (`Fact_PharmacySales`, `Fact_Demand`, `Fact_Inventory`) with conformed dimensions (DimDate, DimMedicine SCD2, DimFacility, DimWarehouse, DimSalesProfile) as documented in the workbook (sheets typically: Business.Req.XRay, OLTP.XRay, Transform.OLTP, Dim.Tables, Fact.Table.*, Star.Schema with Q1-Q3). Profile 02 and 03 only for lineage/expiry lookups.

**Ground rules for this stage:** write only under `docs/sdi_verification/`, `sql/verification/`, `scripts/`, `data/scratch/`. Every result must come from **one** script `scripts/verify_sdi.py` that regenerates all result files (seed any sampling). Do not edit the workbook here.

### S1.1 Inventory and profile [MUST]
For each source file: row count, columns + inferred types, null % per column, distinct counts, min/max for numeric/date columns, duplicate check on the documented PK, encoding/delimiter issues, whitespace/case anomalies in key and categorical columns. Compare row counts to spec: **63 / 561 / 999 / 112,184 / 500,000 / 27,216** (files 01..06); report any difference. Extract the workbook and mark each dimension/fact column `EXISTS / MISSING / RENAMED:<real name>` → `docs/sdi_verification/00_column_traceability.csv`. Output `01_profile.md`.

### S1.2 Test hypotheses H1-H18 [MUST]
For each: write SQL, run it, save the result CSV, state **PASS / FAIL / PARTIAL / NOT TESTED**, evidence in 1-2 lines, and the decision. Output `02_findings.md` (table: result, evidence, decision, ADR link).

| ID | Hypothesis / test | Decision rule |
|---|---|---|
| H1 | **SCD2 history exists?** More than one row per MedicineID, or varying EffectiveFromDate in 01? | If one version per SKU, SCD2 can't be shown from base data → note that a controlled change fixture (S6.5) and later the generator must inject changes. |
| H2 | **Region derivation.** Workbook assumes "4 US regions" from State. Distinct CountryCode/State/City across pharmacies, hospitals, warehouses; all US? Region column present? | Decide derivation; 100% of facilities and warehouses must map (no unknowns). |
| H3 | **Channel semantics.** Distinct SalesChannel and PharmacyType + cross-tab; which rows are the "Hospital" channel; which ID (PharmacyID/HospitalID) is populated. | Decide number of channels (2 or 3), DimChannel design, and whether Q1 must exclude hospital-channel sales. |
| H4 | **Conformed DimFacility feasibility.** Do PharmacyID and HospitalID share a format? ID overlap/collisions? Are hospital IDs in 05 the same as in 06? | Union into DimFacility with a type attribute, or keep DimHospital/DimPharmacy separate. |
| H5 | **Junk dimension size.** Distinct combinations of (PrescriptionRequiredFlag, CustomerSegment, PayerType, PaymentMethod, PromotionCode, SaleStatus, ReturnFlag); PromotionCode cardinality alone. | If combinations > ~500 or PromotionCode high-cardinality/time-varying → separate DimPromotion; else one junk dim. |
| H6 | **Return representation.** Consistency of ReturnFlag, SaleStatus, ReturnedQuantityPacks; `ReturnedQuantityPacks <= QuantitySoldPacks` everywhere? | Pick the authoritative field; decide whether flags are redundant in the junk dim. |
| H7 | **Warehouse dimension grain.** Within WarehouseID do WarehouseName, GLN, capacity, status stay constant over time? Do StorageZoneID/StorageCondition vary within a warehouse? | If zone varies → DimStorageZone (or zone-grain warehouse). If capacity/status vary over time → SCD2 on those. |
| H8 | **Hospital attributes.** Per HospitalID, are LicensedBeds, ICUBeds, TraumaLevel, CatchmentPopulation constant? Where are MedicationRequestStatus/FormularyStatus used (per row or per hospital)? Same test for InventoryStatus/WarehouseActivityStatus. | Row-varying low-cardinality status → junk dim (DimDemandProfile / DimInventoryStatus); per-entity constant → DimFacility/DimWarehouse. |
| H9 | **DimMedicine columns.** Every OLTP.XRay column for 01 exists; WholesalePriceUSD, StorageMinTempC, StorageMaxTempC, ShelfLifeMonths carried into the dimension (workbook Dim.Tables may omit them and EffectiveFrom/To); StorageMin < StorageMax; costs/prices > 0; ColdChainFlag consistent with temperature range. | List missing columns for the workbook change list. |
| H10 | **Sales arithmetic.** Gross = Qty × UnitPrice; Net = Gross − Discount; Margin = Net − COGS (tolerance 0.01). COGS vs Qty × UnitManufacturingCostUSD (point-in-time if history). | Per measure: load source value, or recompute and log the delta in DQ. |
| H11 | **Sales grain and lineage.** SalesTransactionID unique? % of WarehouseLotID resolving to 04; ProductionBatchID resolving to 02; one WarehouseLotID ↔ one WarehouseID?; sale's medicine = lot's medicine? | Report orphan counts; set DQ rules. |
| H12 | **DaysToExpiryAtSale.** Source value vs (lot expiry date − SaleDate), where lot expiry = snapshot date + DaysToExpiry from 04, or batch expiry from 02. | Choose the authoritative expiry source; report % match and typical error. |
| H13 | **Demand grain and measures.** HospitalDemandRecordID unique; (HospitalID, MedicineID, Month) unique; month key format; UnfulfilledDemandPacks vs GREATEST(0, Requested−Received) / GREATEST(0, Requested−Consumed); ServiceLevelPct vs Received/Requested and Consumed/Requested; stock identity Opening + Received − Consumed − Wastage = Closing (and a Dispensed variant). | If Unfulfilled matches Requested−Received in ≥99% → define fulfilment as Received/Requested and use the source column; if it matches Requested−Consumed → document that; else keep source column "source-defined, unreconciled". |
| H14 | **Inventory grain and density.** (WarehouseLotID, WarehouseID, SnapshotDate) unique? Dense (every lot daily) or sparse? Per warehouse first/last snapshot and missing days. | Decide "latest snapshot" per lot and warehouse, not global MAX(date). |
| H15 | **DaysToExpiry semantics.** Within a lot, does DaysToExpiry fall by exactly the date difference (as-of snapshot) or stay static? Derived ExpiryDate (= SnapshotDate + DaysToExpiry) constant per lot? | Confirm/refute: DaysToExpiry stored as-of SnapshotDate, never recomputed vs today. |
| H16 | **Inventory flags and identity.** StockoutFlag vs (AvailableQuantity = 0); NearExpiryFlag vs (DaysToExpiry <= 90); FEFOComplianceFlag grain/distribution by warehouse; movement identity Closing = Opening + Received − Shipped − Expired − Damaged ± Adjustment (find the version that holds, % failing). | Decide which extra quantity columns Fact_Inventory needs so the identity is testable. |
| H17 | **Cross-file regional consistency.** Pharmacy region = lot's warehouse region? Hospital region vs warehouse region? | Defines what "region" means in Q1 and whether commercial-vs-hospital comparison at region grain is meaningful. |
| H18 | **Date coverage.** Min/max date per file, months present vs expected (2023-2025 must be fully covered); list gaps. | Document gaps. |

### S1.3 Test the workbook's three queries on a throwaway prototype [MUST]
Build a quick prototype star in `data/scratch/sdi_proto.duckdb` from the files using the workbook logic (simple surrogate keys). This is a **test harness only**. Run Q1, Q2, Q3 **exactly as written** in the workbook; record runs/errors (exact error text), row counts, silent logic problems. Confirm or refute **by experiment** these suspicions:
- **a)** Q1: `ORDER BY MonthNumber` ambiguous (both CTEs expose it) → expect a Binder error.
- **b)** Q1 includes hospital-channel sales although the text says pharmacy + e-commerce only → quantify overlap in units.
- **c)** Q2 joins sales velocity and inventory on MedicineSK; with SCD2 versions this splits velocity and drops inventory rows → demonstrate with a medicine that has 2 versions (create a synthetic version row in the prototype if none exist, and say so).
- **d)** Q2 ranks on sales only although the text says "high hospital demand OR high sales"; uses a global MAX(DateKey) snapshot → count warehouses lacking that date.
- **e)** Q3 takes "channel" from FacilityType (compare with SalesChannel); `AVG(DaysToExpiryAtSale)` is per-transaction → compare with the pack-weighted average and report the gap.

Write corrected **Q1', Q2', Q3'** (`sql/verification/q1_fixed.sql`, ...) fixing every confirmed issue. Reconcile: Q1' units (pharmacy + e-commerce only) = SUM raw 05 with the same filter; Q1' hospital quantities = SUM raw 06 (no fan-out); Q3' totals (sales, margin, units) = raw 05 totals; Q2' non-empty and explainable, with 5 sample rows hand-verified against raw data. Write them in **portable ANSI SQL where possible**, because Stage 7 must re-run them on Postgres (note any dialect-specific bits). Output `03_query_test_report.md`.

### S1.4 Documentation-risk review of the workbook [SHOULD]
Business.Req.XRay: list every statistic, dollar figure, percentage, named case study/reference; mark each **SOURCED** (URL you actually opened and read), **UNSOURCED**, or **UNVERIFIABLE**. Never "confirm" from memory. If you have no web access, mark UNVERIFIED. Propose removing/rewording every unsourced figure. Flag unprofessional/off-scope text (e.g., the OLTP.XRay "reason" line; KPIs needing files outside this mart such as OTIF, which needs 03). Check the diagram: clipped? role-playing dates shown? matches Dim.Tables/Fact sheets? List mismatches. Output `05_doc_risk_review.md`.

### S1.5 Change lists [MUST]
- `04_workbook_change_list.md`: precise sheet/cell-level edits for workbook v01 (add/change/remove), each tied to a finding. Another engineer must be able to apply it without reading anything else.
- `06_generator_requirements.md`: what the future data generator must produce because of the findings (SCD2 changes, defect injection, lineage rules, volumes).

### S1.6 ADRs [MUST]
Group findings into roughly **8-15 ADRs** (not 40). Format in Section 10. Prove sources and workbook unchanged (checksums before/after).

**DoD:** `docker compose run --rm tools python scripts/verify_sdi.py` regenerates every result with no manual step; every H1-H18 has a status with evidence or `NOT TESTED` + reason; Q1'/Q2'/Q3' run and reconcile (numbers shown); change list is specific enough for someone else to apply; checksums unchanged. **Then continue to Stage 2.** Do not build the pipeline before Stage 2 is done.

---

## 7. STAGE 2: Workbook v01 (~2 h) [MUST]

| Step | Task |
|---|---|
| S2.1 | Copy workbook to `excel/DAWH_DWH_Pharma_ColdChain_Sales_Demand-01.xlsx` (keep `-00` untouched). Apply **every** item of `04_workbook_change_list.md` with **openpyxl**, preserving formatting. Check that nothing else (images/shapes) is lost on save, and report. |
| S2.2 | Add a **Changelog** sheet (change, source finding/ADR, before/after). Keep sheet names/layout (Dim.Tables, Fact.Table.PharmSales (rename if needed and say so), Fact.Table.Demand, Fact.Table.Inventory, Star.Schema). Add a Role-Playing section; mark junk dimensions and bridge tables if any. Replace the 3 queries with verified Q1'/Q2'/Q3', each with a "Result evidence" row (row count, 3-5 sample rows, reconciliation numbers). Business.Req.XRay: remove/reword every UNSOURCED/UNVERIFIABLE claim; keep only claims with a source you opened (with URL); replace the unprofessional line; move out-of-scope KPIs (e.g., OTIF) to a "Later phases" note. |
| S2.3 | Regenerate the star-schema diagram in Python (matplotlib/SVG→PNG in the tools container): not clipped, matches the sheets exactly, shows role-playing dates (sale / snapshot / demand month / expiry), junk dimensions, every FK. Embed in Star.Schema. Re-run the column traceability check and attach the result. |

**DoD:** workbook opens without errors; every dimension/fact column traces to a real source column or documented derivation (`docs/sdi_verification/workbook_v01_traceability.csv`).

---

## 8. STAGES 3-8: Production pipeline (Prompt B)

### STAGE 3: Docker platform (~2-3 h) [MUST]

| Step | Task |
|---|---|
| S3.1 | Verify and pin versions (rule 3.1); finalize ADR-002. |
| S3.2 | `docker-compose.yml` with: **postgres** (persistent named volume; databases `airflow` (metadata) and `dwh`; schemas `bronze`, `silver`, `gold`, `dq`, `obs`); **airflow** webserver/api-server + scheduler (+ dag-processor if the pinned version needs it), LocalExecutor, example DAGs disabled; **prometheus**; **pushgateway**; **grafana** with **provisioned** datasources (Prometheus **and** Postgres) and dashboards from `config/`; **tools**. Health checks, restart policies, named volumes, dedicated network. Airflow image: pinned Airflow + providers + pandas/openpyxl/psycopg + **dbt-postgres in an isolated venv** (`/opt/dbt-venv`). Source dir mounted **read-only** into Airflow and tools. dbt project and `include/` mounted into Airflow. |
| S3.3 | Postgres init DDL (`sql/ddl/`): schemas; `bronze.load_manifest`; `dq.rejected_rows`; `obs.query_log` (columns: `ts, query_id, dashboard, widget, engine, run_label, duration_ms, rows_returned, status, error_text, optimized_flag`) with timestamp indexes. Airflow connections/variables from environment. |
| S3.4 | Hello-world DAG proving: DB connection, `dbt debug` via the venv, access to the read-only source mount. |

**DoD:** `docker compose up -d` → all services `healthy` (`docker compose ps` pasted to `docs/commands.md` evidence); Airflow, Grafana and Prometheus UIs reachable; Grafana datasource tests pass; `make down && make up` preserves Postgres data. Record URLs/ports in `docs/commands.md`.

### STAGE 4: Python loader → PostgreSQL Bronze (~3 h) [MUST]

| Step | Task |
|---|---|
| S4.1 | `docs/bronze/source_inventory.md`: for each input file/sheet: expected table, business key, row count, columns, types; checksums computed **before** ingestion. |
| S4.2 | `scripts/load_bronze.py` (logic in `include/ingestion/`): reads actual Excel/CSV, creates `bronze.<table>` tables. **All source columns stored as TEXT, values faithful.** No cleaning, dedup, filtering or business transformation. The only technical rule is empty cell → NULL (document it in an ADR; dates/numbers from Excel converted to text deterministically, documented). Add technical columns: `_batch_id, _source_file, _source_sheet (nullable), _ingested_at, _source_row_number, _source_checksum`. Chunked inserts / `COPY`; transaction per file/sheet. |
| S4.3 | `bronze.load_manifest`: batch id, file, sheet, checksum, start/end timestamps, source row count, loaded row count, status, error details. **Idempotent:** same unchanged file/sheet (checksum + source identity) → skipped and logged as `duplicate`/`already_loaded`, no duplicate rows. A **changed** file → new batch, history never overwritten. Failed required input → recorded and non-zero exit code. |
| S4.4 | `scripts/check_bronze.py`: table existence, source-vs-Bronze row counts for every file/sheet, metadata present, duplicate-ingestion prevention, manifest status. Add indexes only on technical/business keys that are justified. |
| S4.5 | Tests (pytest, in tools): load all files; reload (expect no change); corrupt-file test (expect `failed` + non-zero exit, then success after fix); prove source checksums unchanged. |

**DoD:** Bronze row counts = source rows for every file/sheet (table pasted to `docs/bronze/load_manifest_evidence.md`); second run changes nothing; failure path demonstrated.

### STAGE 5: Airflow DAG `dag_mart_sdi` (~2 h) [MUST]

Required ordered tasks (TaskGroups allowed):
`check_source_files → load_excel_to_postgres_bronze → validate_bronze_load → profile_bronze → dbt_build_silver → dbt_build_gold → run_q1_q3_acceptance_tests → publish_ingestion_metrics`
(Stage 9 inserts `run_query_benchmark` after the acceptance tests.)

Requirements: retries + retry delay, task timeouts, clear logs, failure reporting (`on_failure_callback` writes an event); a failed Bronze load/validation prevents any dbt task; safe reruns/backfills via loader idempotency (a retry must not re-ingest); credentials via env/connections only. Provide `docs/airflow_dag.md` with the task dependency explanation (and a graph screenshot if possible). Initially tasks after `profile_bronze` may be stubs; replace them as Stages 6-8 complete.

**DoD:** one successful DAG run through the implemented tasks; a deliberately failed Bronze load blocks downstream tasks (evidence saved).

### STAGE 6: Profile Bronze, then dbt Silver and Gold in PostgreSQL (~6-8 h) [MUST]

| Step | Task |
|---|---|
| S6.1 | `profile_bronze` (script and DAG task): profile the **landed PostgreSQL Bronze tables** (not the files, not DuckDB): row counts, columns/types, nulls, distinct counts, duplicate business keys, date ranges, source→Bronze reconciliation → `docs/bronze/bronze_profile.md`. |
| S6.2 | dbt project with **dbt-postgres**, `profiles.yml` from environment variables, a `generate_schema_name` override so schemas are exactly `silver` / `gold` / `agg` (no `public_` prefixes). Register Bronze tables as **dbt sources**. **No Silver/Gold model may read directly from files.** |
| S6.3 | **Silver:** typed, trimmed, deduped (latest by `_ingested_at` per natural key). Apply DQ rules from ADRs: price > 0, valid dates, expiry > manufacture, non-null keys, non-negative quantities, return ≤ sold, arithmetic identities within tolerance. Rejected rows → documented rejects table with reason codes; never drop silently. |
| S6.4 | **Gold must match workbook v01 column-for-column:** `dim_date` (YearMonth, MonthStartDateKey, role-playing date relationships), `dim_medicine` (**SCD Type 2 via dbt snapshot**, ValidFrom/ValidTo, point-in-time lookups), `dim_facility` and the other dims as decided in the ADRs, an **unknown member (-1) in every dimension**, and `fact_pharm_sales`, `fact_demand`, `fact_inventory` at their documented grains. **DaysToExpiry is stored AS OF SnapshotDate with ExpiryDateKey; never recomputed vs today.** Incremental where appropriate; documented strategy for late-arriving data and changed batches. |
| S6.5 | **SCD2 proof.** If H1 showed no history in the base data: create a small, clearly labelled **test fixture** (e.g., `data/test_fixtures/01_master_scd2_delta.xlsx|csv`: a copy of a few 01 rows with one changed attribute such as price/storage range), ingest it through the **same loader as a new batch**, never touching the source files, and document that the real change generator comes later. Prove: one medicine with two versions, and sales rows pointing to the correct version **by date**. |
| S6.6 | dbt tests: `unique`, `not_null`, `relationships`, `accepted_values`, custom DQ tests including **SCD2 non-overlap** and the **inventory movement identity** decided in Stage 1. **Reconciliation tests (in `tests/` or dbt singular tests):** Bronze source rows = Silver accepted + rejects; Silver = Gold per fact; measure sums reconcile to the agreed source definitions. |

**DoD:** `dbt build` green; reconciliation numbers pasted to `docs/reconciliation.md`; **a second `dbt build` with no new data changes nothing** (row counts before/after shown); workbook v01 vs Gold column check passes (`scripts/check_workbook_vs_gold.py`, can also run as CI-style check).

### STAGE 7: Q1-Q3 as acceptance tests (~2 h) [MUST]

1. Put Q1', Q2', Q3' in `sql/bench/` with a tag line on each query: `-- dashboard: <page>; widget: <name>`. Port from the verified dialect to Postgres and re-reconcile.
2. Run them on **Gold**. Each returns a non-empty result and reconciles to raw (show the numbers): Q1' units = raw 05 filtered sum, hospital quantities = raw 06 sum, no fan-out; Q3' totals = raw 05 totals; Q2' returns hand-verified sample rows.
3. Add a test that **fails** if any benchmark/acceptance query uses `MedicineSK` in a cross-fact join (must use the natural key or the current-version rule), so the SCD2 trap cannot return.
4. Wire them into the DAG task `run_q1_q3_acceptance_tests`.

**DoD:** all three pass in the DAG with numbers saved to `docs/q_acceptance.md`; the SK-misuse test fails when you inject a bad query and passes otherwise.

### STAGE 8: Ingestion observability: Prometheus + Pushgateway + Grafana (~3 h) [MUST]

Metrics (real values only, no hard-coded or fabricated data):

| Metric | Labels |
|---|---|
| `sdi_ingestion_files_total` | status |
| `sdi_ingestion_rows_total` | source/table, status |
| `sdi_ingestion_duration_seconds` | source/table |
| `sdi_ingestion_rows_per_second` | source/table |
| `sdi_ingestion_failures_total` | source/table, reason_category |
| `sdi_ingestion_last_success_timestamp` | source/table |
| `sdi_ingestion_batch_status` | batch (bounded labels only; never full paths or arbitrary error text) |

Rules: emit on success **and** failure; **retries must not inflate success counters.** State clearly whether each counter counts *attempts* or *committed loads* (recommended: derive cumulative success totals from `bronze.load_manifest` at publish time, since Pushgateway keeps the last pushed value). Prometheus scrapes Pushgateway; Grafana is **provisioned** from `config/` with a dashboard JSON showing: files loaded/failed, rows loaded, ingestion duration (horizontal bar per source), throughput, failures, last successful ingestion, batch status; with time filter and source/table filter. Write a **metric dictionary** (name, type, labels, meaning, emission point, unit) in `docs/metrics_ingestion.md`.

**DoD:** the dashboard shows real values from a real successful load **and** a controlled failed-file test (Prometheus queries + screenshots or exported dashboard JSON saved in `docs/bronze/`). Do not claim this done until real values are visible in Grafana.

---

## 9. STAGE 9: THE QUERY LAYER + OPTIMIZATION (~4 h) [MUST]

This is the target of the current work. The query layer is **the canonical, tagged analytical queries over Gold, a benchmark harness that times and logs them, measured optimization, and a performance dashboard.** (It is *not* the semantic layer.)

| Step | Task | Tag |
|---|---|---|
| S9.1 | **Canonical query catalogue** in `sql/bench/`: every dashboard widget query lives here, tagged `-- dashboard: X; widget: Y`. Minimum **≥ 10 widget queries over ≥ 4 pages**: **Q1** page "Sales vs Hospital Demand" (units sold vs requested/received/consumed, unfulfilled demand by disease and region, forecast vs actual); **Q2** page "Stockout & Expiry Exposure" (warehouse/lot drill-down, near-expiry, expired qty, FEFO %); **Q3** page "Commercial Profitability" (net sales, gross margin, return rate, days-to-expiry-at-sale by channel/segment/payer/promotion); **Supporting** page "Fast vs Slow movers by therapeutic class" (document the velocity definition) + KPI cards. Ratios always `SUM(num)/SUM(den)`; inventory balances semi-additive. These exact queries will later power the Superset datasets. | MUST |
| S9.2 | **Benchmark harness** `scripts/run_bench.py` (logic in `include/bench/`): parses tags, runs each query N times (default 5, configurable) with `time.perf_counter()`, writes **one row per run** to `obs.query_log` (`status`, `error_text`, `rows_returned`, `run_label` = `baseline`/`optimized`, `optimized_flag`). Errors are caught and logged, not fatal. Add the DAG task **`run_query_benchmark`** (after `run_q1_q3_acceptance_tests`). | MUST |
| S9.3 | **Baseline** run first, before any optimization; record volumes (row counts per fact/dim) in `docs/query_optimization.md`. | MUST |
| S9.4 | **Optimize, measured before/after** (`EXPLAIN (ANALYZE, BUFFERS)` plans saved before and after in `docs/query_optimization.md`): pre-aggregated `agg_*` tables built by dbt (or dbt materialized views) refreshed incrementally; B-tree indexes on join keys and date keys, **BRIN** on large date-ordered facts where it helps; composite/covering indexes for the worst queries; `ANALYZE` after loads; clustering/sorting by date where justified; join-order and filter-pushdown rewrites on the **worst two queries**; avoid cross-fact joins before aggregation (aggregate each fact separately, then join). Do not add indexes without measuring. After optimization, re-run the benchmark with `run_label='optimized'`. Re-run Stage 7 acceptance tests: optimized queries must return **identical results**. | MUST |
| S9.5 | **Grafana "Query Performance" dashboard** (Postgres datasource on `obs.query_log`, provisioned as JSON in `config/`): average execution time per widget (column/bar chart), daily query count, error rate (failed ÷ executed), p95 duration, **before vs after optimization** comparison, and a recent-errors table. | MUST |
| S9.6 | Optional "chaos" toggle: one clearly labelled malformed query to show error-rate capture. | COULD |
| S9.7 | Also record the real query count from the BI tool's own metadata later when Superset exists (out of scope now). | COULD |

**DoD (query layer):**
- The two slowest queries show a **documented speed-up** (before/after numbers + plans).
- **All widget queries < 1 s** at current volumes (state the volumes).
- `obs.query_log` has **≥ 50 rows across ≥ 8 widgets**, including at least one logged error row if S9.6 was done.
- Grafana Query Performance dashboard shows real data (screenshot or exported JSON saved).
- Optimized and baseline results are identical (proof saved).

---

## 10. DECISION RECORDS (ADRs)

One file per decision in `docs/decisions/NNN-title.md`, numbered continuously. Format: **Title · Context · Hypothesis tested · Evidence (SQL file + result file + key numbers) · Options considered · DECISION · Consequences for model / DQ rules / generator · Confidence (HIGH/MEDIUM/LOW) and what would change your mind.** Group related findings; aim for ~8-15 for Stage 1 plus a few for platform choices.

---

## 11. STAGE 10: Close-out (~1-2 h)

| Step | Task | Tag |
|---|---|---|
| S10.1 | **Clean-clone test:** in a fresh directory, `git clone` (or copy) → `.env` from `.env.example` → `make up` → `make load-base` → DAG run → `make bench`. Fix anything that needs manual steps. | MUST |
| S10.2 | `README.md`: prerequisites (Docker only), 5-command quickstart, ports/URLs, how to resume from `PROGRESS.md`. | MUST |
| S10.3 | `docs/metrics.md`: SDI metric dictionary (net sales, gross margin %, return rate, discount penetration, hospital fulfilment, forecast-to-actual, WAPE, unfulfilled demand rate, days of cover, stockout rate, near-expiry value at risk, FEFO %, expiry waste %): definition, formula, grain, additivity, source. Ratios = SUM(num)/SUM(den); inventory balances semi-additive. | SHOULD |
| S10.4 | Generator spec stub for SDI based on `06_generator_requirements.md` (what to generate for refresh R1/R2: volumes, SCD2 changes, defect rates, lineage rules). | SHOULD |
| S10.5 | Final `PROGRESS.md`: everything `DONE` or explicitly listed as not done with reasons; tag `iter-sdi-v01` (`git tag`). Final report: **Done · Evidence · Assumptions · Open questions · Risks to 25 Nov · Next.** | MUST |

### FINAL DEFINITION OF DONE (whole scope)
1. `docker compose up -d` starts everything healthy.
2. One successful Airflow `dag_mart_sdi` run: Excel/CSV → PostgreSQL Bronze → validate → profile → dbt Silver → dbt Gold → Q1-Q3 acceptance → query benchmark → metrics published.
3. Bronze and `bronze.load_manifest` contain real data; source→Bronze counts and checksums reconcile.
4. `dbt build` green with reconciliation tests passing; second build changes nothing.
5. Workbook v01 and Gold match column-for-column.
6. Q1', Q2', Q3' pass and reconcile; SCD2 point-in-time proof shown.
7. Prometheus/Grafana show real ingestion metrics; Grafana Query Performance dashboard shows real `obs.query_log` data.
8. The two slowest queries have documented optimization; all widget queries < 1 s.
9. Sources and workbook `-00` unchanged (checksum proof).
10. `PROGRESS.md` accurate and a new agent could resume from it alone.

---

## 12. OUT OF SCOPE (do not build now; do not mark as missing)

Superset business dashboards; the causal data generator and the two live refreshes (R1/R2); Phase 2 (Inventory/Expiry/Replenishment) and Phase 3 (Traceability/IoT) marts; the fact-constellation integration and semantic layer (`sem_*`, MetricFlow); streaming ingestion; file-watcher/FastAPI ingestion service; Redpanda/Kafka. Prepare cleanly for them (conformed dimensions, tagged queries, generator spec stub), but build none of them.

---

## 13. WHEN TO ASK THE HUMAN vs DECIDE

Decide and log an ADR when the choice is reversible. Ask only when blocked by: missing files, Docker unusable, credentials, instructor-defined ambiguity (e.g., Excel vs CSV expected at demo), or an irreversible action. When you ask, include your recommendation and continue with any work that does not depend on the answer.

---

## APPENDIX A: Starter prompt for the human to paste (first session)

```
You are working in the repo at <path>. Read AGENTS.md fully, then PROGRESS.md (if it exists).
Execute AGENTS.md from Stage 0 onward, working continuously through the stages in order.
Everything must run in Docker. Update PROGRESS.md after EVERY step as AGENTS.md Section 2 requires,
and commit after every step. Source files are at <path-to-source-files>; the workbook is at <path-to-workbook>.
Human decisions so far: <none / list>. Hours available today: <n>.
Stop only for true blockers or after Stage 10.
```

## APPENDIX B: Handoff prompt for a NEW agent (after an account/context limit)

```
You are continuing an in-progress project in the repo at <path>. You have no memory of earlier work.
1. Read AGENTS.md (the full instruction set), then PROGRESS.md, starting with "RESUME HERE".
2. Read docs/decisions/ titles and docs/commands.md. Run `docker compose ps` to learn the real state.
3. Reconcile PROGRESS.md with reality (fix it if wrong), then continue from the exact next action.
4. Do not redo DONE steps unless their evidence is missing or a check fails.
5. Keep updating PROGRESS.md after every step and commit after every step.
Human decisions since last session: <none / list>.
```
