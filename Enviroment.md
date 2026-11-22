\# 01 — ENVIRONMENT & DISCOVERY

\*\*Goal:\*\* a working Docker stack \+ a complete understanding of the 7 CSVs (the agent was NOT given the schemas; it must discover them).  
\*\*Prereq:\*\* none. \*\*Next:\*\* \`02\_SDI\_EXCEL.md\`.

\#\# 🛑 ASK HUMAN (one message, wait for answers)  
1\. Are the 7 CSVs in \`data/raw/\`? (If not: ask to place them; do not proceed to profiling without at least files 01, 05, 06.)  
2\. Exact deadline of the \*current\* submission and which submission is due first (A: query layer / B: BI)? (Default: portal due Sun 22 Nov 2026 23:55 PKT, submit A and B together.)  
3\. Is the OS Windows with Docker Desktop (WSL2) \+ Power BI Desktop installed? Is the repo inside WSL2?  
4\. GitHub repo URL; may large files go in the repo? (Default: raw CSVs and DuckDB excluded via \`.gitignore\`; generator \+ \`make seed\` recreate everything.)  
5\. Group member names/IDs (write to \`docs/group\_members.md\`).

\#\# Tasks  
\#\#\# 1.1 Scaffold  
Create the layout in Master Playbook §3, \`.gitignore\` (\`.env\`, \`\*.duckdb\`, \`pgdata/\`, \`airflow/logs/\`, \`data/landing/\*\`, \`data/archive/\*\`, \`data/raw/\*.csv\` unless human says otherwise, \`\_\_pycache\_\_\`, \`.venv\`), \`.gitattributes\`, \`.env.example\` (POSTGRES\_USER/PASSWORD/DB, AIRFLOW\_UID=50000, FERNET\_KEY, API\_PORT=8000, WATCH\_INTERVAL\_S=2), \`Makefile\` with targets: \`up, down, logs, psql, seed, refresh, test, reset\` (reset \= \`docker compose down \-v\`, dangerous: ask before running).  
\`git init\`, first commit.

\#\#\# 1.2 Docker stack (\`docker-compose.yml\` \+ \`docker/Dockerfile\`)  
Services: \`pharma-db\` (postgres:16, host 5433, healthcheck \`pg\_isready\`, init scripts from \`sql/postgres/\`), \`airflow-db\` (postgres:16), \`airflow-init\` (db migrate \+ create admin user \`admin/admin\`), \`airflow-webserver\` (8080), \`airflow-scheduler\`, \`ingest-api\` (uvicorn pipeline.ingestion.api:app, 8000), \`file-watcher\` (python \-m pipeline.ingestion.watcher).  
Dockerfile: base \`apache/airflow:2.10.5-python3.11\`; as root install \`build-essential libpq-dev graphviz\`; as airflow user: \`pip install\` pipeline requirements; create venv \`/opt/dbt-venv\` with \`dbt-core dbt-duckdb\`; pre-install DuckDB extensions (\`python \-c "import duckdb;c=duckdb.connect();c.sql('INSTALL postgres')"\` for both the main python and the dbt venv). Set \`PYTHONPATH=/opt/airflow:/opt/airflow/pipeline\_root\` so \`import pipeline...\` works. Mount: \`./pipeline\`, \`./airflow/dags\`, \`./dbt\_sdi\`, \`./warehouse\`, \`./data\`, \`./sql\`.  
Use \`LocalExecutor\`, \`AIRFLOW\_\_CORE\_\_LOAD\_EXAMPLES=false\`.

\#\#\# 1.3 Verify stack (acceptance)  
\`\`\`  
docker compose up \-d \--build  
docker compose ps                         \# all Up/healthy  
docker compose exec pharma-db psql \-U \$POSTGRES\_USER \-d pharma \-c "\\dn"   \# schemas stg, meta, bi exist (from 001\_schemas.sql)  
curl \-s localhost:8000/health             \# {"status":"ok"}  
curl \-s \-o /dev/null \-w "%{http\_code}" localhost:8080/health   \# 200  
docker compose exec airflow-scheduler airflow dags list         \# no import errors  
\`\`\`  
If the API module does not exist yet, create a stub \`/health\` now; Stage 4 completes it.

\#\#\# 1.4 Profile the data (no assumptions\!)  
Write \`pipeline/profiling/profile\_csv.py\` (pandas, chunked for big files) and run it for all 7 CSVs. For \*\*each file\*\* record in \`docs/data\_profile.md\`:  
row count; columns with inferred dtype; null count/%; distinct count; min/max (numeric & date); top-5 values for low-cardinality columns; candidate PK uniqueness check (is the documented PK really unique?); date column ranges; negative/zero values in price/quantity columns; duplicated rows.  
