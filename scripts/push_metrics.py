"""
scripts/push_metrics.py
Publishes ingestion metrics from bronze.load_manifest to Prometheus Pushgateway.
"""

import os
import sys
import psycopg
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB   = os.getenv("POSTGRES_DB", "dwh")
POSTGRES_USER = os.getenv("POSTGRES_USER", "pharma_admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "pharma_secret_pw")
PUSHGATEWAY_URL = os.getenv("PUSHGATEWAY_URL", "pushgateway:9091")

CONN_STR = f"host={POSTGRES_HOST} port={POSTGRES_PORT} dbname={POSTGRES_DB} user={POSTGRES_USER} password={POSTGRES_PASSWORD}"

def main():
    conn = psycopg.connect(CONN_STR)
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT ON (target_table) 
            target_table, row_count, execution_time_seconds, status
        FROM bronze.load_manifest
        ORDER BY target_table, loaded_at DESC;
    """)
    rows = cur.fetchall()

    registry = CollectorRegistry()
    g_rows = Gauge('dwh_bronze_rows_loaded_total', 'Total rows loaded into Bronze table', ['table'], registry=registry)
    g_time = Gauge('dwh_bronze_load_duration_seconds', 'Ingestion duration in seconds', ['table'], registry=registry)
    g_status = Gauge('dwh_bronze_load_status', '1 if load successful, 0 otherwise', ['table'], registry=registry)

    for tbl, r_cnt, duration, status in rows:
        g_rows.labels(table=tbl).set(r_cnt)
        g_time.labels(table=tbl).set(float(duration or 0.0))
        g_status.labels(table=tbl).set(1 if status == 'SUCCESS' else 0)
        print(f"  Pushed {tbl}: {r_cnt:,} rows, {duration}s, status={status}")

    push_to_gateway(PUSHGATEWAY_URL, job='bronze_loader', registry=registry)
    print("Successfully pushed latest manifest metrics to Pushgateway!")
    conn.close()

if __name__ == "__main__":
    main()
