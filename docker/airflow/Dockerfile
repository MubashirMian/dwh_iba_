FROM apache/airflow:2.10.5-python3.11

USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow
RUN pip install --no-cache-dir \
    dbt-core==1.8.7 \
    dbt-postgres==1.8.2 \
    duckdb==1.1.3 \
    psycopg[binary]==3.2.3 \
    prometheus-client==0.21.0 \
    pandas==2.2.3 \
    openpyxl==3.1.5
