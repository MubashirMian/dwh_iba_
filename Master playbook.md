\# 00 — MASTER PLAYBOOK (architecture, contracts, conventions)

Read once per session. Every stage manual depends on the decisions fixed here. \*\*Do not re-decide these\*\*; if you must deviate, log it in \`ASSUMPTIONS.md\` and update this file.

\#\# 1\. What is being graded (design everything to hit these)  
\| Item \| Weight \| Where it is delivered \|  
\|---\|---\|---\|  
\| Oversampling (generator on Airflow \+ 1–2 pp PDF report) \| 2% \| Stage 3 \|  
\| Batch ingestion dashboard \| 2% \| Stage 4 data, Stage 8 dashboard \|  
\| Streaming ingestion dashboard \| 2% \| Stage 4 data, Stage 8 dashboard \|  
\| Storage dashboard \| 2% \| Stage 4 data, Stage 8 dashboard \|  
\| Query dashboard \| 2% \| Stage 6 data, Stage 8 dashboard \|  
\| Excel file per phase (\*\*most marks\*\*, "as much info as possible") \| 2.5% each \| Stage 2 \+ 9 \|  
\| Transformation & dimensional modelling \| 2.5% \| Stage 5 \|  
\| BI \| 10% \| Stage 8 \|  
\| Bonus constellation \| 3–4% \| Stage 10 \|  
Also graded: modular Airflow DAGs (clean task separation); dashboards visibly change with new data in a live run; report lists \*\*all assumptions\*\* and the \*\*story\*\* of each dashboard; DWH is \*\*cumulative\*\* (never emptied; history is kept).

\#\# 2\. Fixed architecture  
\`\`\`  
generator (Airflow task) ─► data/landing/\*.csv ─► file-watcher ─► FastAPI ingest ─► Postgres  stg.\*  (ODS/staging)  
iot stream producer (Airflow task) ─► FastAPI /ingest/stream ─► stg.iot\_\* (micro-batches)  
Postgres stg.\* ─► DuckDB (warehouse/sdi.duckdb) via dbt-duckdb: dims, facts, aggregates (star / constellation)  
DuckDB marts ─► publish ─► Postgres bi.\* (mirror for Power BI)      meta.\* \= pipeline/ingestion/storage/query metrics  
Power BI Desktop (Postgres connector, DirectQuery) ─► 4 DE dashboards \+ SDI BI dashboard  
Airflow orchestrates everything; DAG files only wire tasks, logic lives in \`pipeline/\`.  
\`\`\`  
Tech pins: Airflow \*\*2.10.x\*\* (python 3.11, LocalExecutor), Postgres \*\*16\*\*, DuckDB latest stable, dbt-core \+ dbt-duckdb (in a \*\*separate venv\*\* \`/opt/dbt-venv\` inside the image to avoid Airflow dependency conflicts), FastAPI \+ uvicorn, watchdog (\*\*PollingObserver\*\*, 2 s interval — inotify is unreliable on Docker Desktop bind mounts), pandas, psycopg2-binary, SQLAlchemy, numpy, scipy, faker (optional), openpyxl, graphviz, reportlab or weasyprint/pandoc for PDFs.

Windows note: assume Docker Desktop \+ WSL2. Keep the repo inside the WSL2 filesystem if possible (faster bind mounts). Use LF line endings (\`.gitattributes\`: \`\* text=auto eol=lf\`).

\#\# 3\. Repo layout (create in Stage 1\)  
\`\`\`  
GEMINI.md  PROGRESS.md  HUMAN\_TODO.md  ASSUMPTIONS.md  README.md  Makefile  .env.example  .gitignore  .gitattributes  
docker-compose.yml  
docker/Dockerfile                      \# one image for airflow \+ ingest-api \+ watcher \+ tools  
manuals/                               \# these manuals  
data/raw/ landing/ archive/ rejected/ generated/   \# raw \= original CSVs (read-only)  
sql/postgres/001\_schemas.sql 002\_meta.sql 003\_stg.sql 004\_bi.sql  
pipeline/  
  common/ (config.py db.py logging.py timing.py)  
  generator/ (base.py sales.py ... orchestrator.py cli.py)  
  ingestion/ (api.py watcher.py loaders.py validators.py stream\_producer.py)  
  metrics/ (storage.py coverage.py query\_bench.py)  
  publish/ (duck\_to\_pg.py)  
dbt\_sdi/ (dbt\_project.yml profiles.yml models/ snapshots/ tests/ macros/)  
warehouse/                             \# sdi.duckdb (gitignored)  
airflow/dags/  airflow/logs/ (gitignored)  
bi/ sql/ (views) dax/ theme/ specs/ screenshots/ (human adds)  
