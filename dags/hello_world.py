from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="hello_world",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["verification"],
) as dag:
    t1 = BashOperator(
        task_id="print_hello",
        bash_command="echo 'Hello from Pharma Airflow Stack'",
    )
