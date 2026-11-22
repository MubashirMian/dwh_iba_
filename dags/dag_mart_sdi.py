"""
dags/dag_mart_sdi.py
Orchestration DAG for Sales & Demand Intelligence (SDI) Mart.
Pipeline stages:
  1. task_bronze_ingest: Execute Python loader to ingest raw CSVs/Excel into bronze tables.
  2. task_check_bronze: Validate row counts and audit columns in bronze.
  3. task_dbt_silver: Run dbt silver models (cleaning, typing, deduplication).
  4. task_dbt_gold: Run dbt gold models (star schema dims and facts).
  5. task_dbt_test: Execute dbt test suite.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "pharma_data_platform",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="dag_mart_sdi",
    default_args=default_args,
    description="End-to-end ELT orchestration for Pharma Cold-Chain SDI Mart",
    schedule_interval=None,  # Triggered on-demand or via upstream events
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["pharma", "sdi", "gold", "dbt"],
) as dag:

    # 1. Ingest Raw Data into Bronze Layer
    task_bronze_ingest = BashOperator(
        task_id="task_bronze_ingest",
        bash_command="python /opt/airflow/scripts/load_bronze.py",
        env={
            "POSTGRES_HOST": "postgres",
            "POSTGRES_PORT": "5432",
            "POSTGRES_DB": "dwh",
            "POSTGRES_USER": "pharma_admin",
            "POSTGRES_PASSWORD": "pharma_secret_pw",
            "PUSHGATEWAY_URL": "pushgateway:9091",
        },
    )

    # 2. Check and Profile Bronze Layer
    task_check_bronze = BashOperator(
        task_id="task_check_bronze",
        bash_command="python /opt/airflow/scripts/check_bronze.py",
        env={
            "POSTGRES_HOST": "postgres",
            "POSTGRES_PORT": "5432",
            "POSTGRES_DB": "dwh",
            "POSTGRES_USER": "pharma_admin",
            "POSTGRES_PASSWORD": "pharma_secret_pw",
        },
    )

    # 3. Transform to Silver Layer (dbt views)
    task_dbt_silver = BashOperator(
        task_id="task_dbt_silver",
        bash_command="cd /opt/airflow/dbt && dbt run --select silver --profiles-dir .",
        env={
            "POSTGRES_HOST": "postgres",
            "POSTGRES_PORT": "5432",
            "POSTGRES_DB": "dwh",
            "POSTGRES_USER": "pharma_admin",
            "POSTGRES_PASSWORD": "pharma_secret_pw",
        },
    )

    # 4. Transform to Gold Layer (dbt star schema tables)
    task_dbt_gold = BashOperator(
        task_id="task_dbt_gold",
        bash_command="cd /opt/airflow/dbt && dbt run --select gold --profiles-dir .",
        env={
            "POSTGRES_HOST": "postgres",
            "POSTGRES_PORT": "5432",
            "POSTGRES_DB": "dwh",
            "POSTGRES_USER": "pharma_admin",
            "POSTGRES_PASSWORD": "pharma_secret_pw",
        },
    )

    # 5. Run dbt Test Suite (constraints, foreign keys, reconciliations)
    task_dbt_test = BashOperator(
        task_id="task_dbt_test",
        bash_command="cd /opt/airflow/dbt && dbt test --profiles-dir .",
        env={
            "POSTGRES_HOST": "postgres",
            "POSTGRES_PORT": "5432",
            "POSTGRES_DB": "dwh",
            "POSTGRES_USER": "pharma_admin",
            "POSTGRES_PASSWORD": "pharma_secret_pw",
        },
    )

    # Set dependency pipeline
    task_bronze_ingest >> task_check_bronze >> task_dbt_silver >> task_dbt_gold >> task_dbt_test
