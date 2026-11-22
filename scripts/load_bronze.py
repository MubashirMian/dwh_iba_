"""
scripts/load_bronze.py
High-performance PostgreSQL Bronze Loader for Pharma Cold-Chain DWH.
Implements:
  - Strict raw fidelity (TEXT columns).
  - Technical audit columns (_loaded_at, _source_file).
  - bronze.load_manifest idempotency (SHA-256 fingerprinting).
  - Pushgateway Prometheus metric emission.
  - Supports both .csv and .xlsx sources.
"""

import os
import sys
import glob
import time
import hashlib
import psycopg
import pandas as pd
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

# Configuration
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB   = os.getenv("POSTGRES_DB", "dwh")
POSTGRES_USER = os.getenv("POSTGRES_USER", "pharma_admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "pharma_secret_pw")
PUSHGATEWAY_URL = os.getenv("PUSHGATEWAY_URL", "pushgateway:9091")

CONN_STR = f"host={POSTGRES_HOST} port={POSTGRES_PORT} dbname={POSTGRES_DB} user={POSTGRES_USER} password={POSTGRES_PASSWORD}"

DATA_DIR = "/workspace/data/source"

FILE_TABLE_MAP = {
    "01_master_data.csv": "bronze.master_data",
    "02_manufacturing_data.csv": "bronze.manufacturing_data",
    "03_manufacturer_delivery_data.csv": "bronze.manufacturer_delivery_data",
    "04_warehouse_data.csv": "bronze.warehouse_data",
    "05_pharmacy_sales_data.csv": "bronze.pharmacy_sales_data",
    "06_hospital_demand_data.csv": "bronze.hospital_demand_data",
    "07_iot_streaming_data.csv": "bronze.iot_streaming_data"
}

def get_file_sha256(filepath):
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            sha.update(chunk)
    return sha.hexdigest().upper()

def load_file_to_bronze(conn, filepath, target_table, force=False):
    fname = os.path.basename(filepath)
    fsize = os.path.getsize(filepath)
    fhash = get_file_sha256(filepath)
    start_time = time.time()
    
    print(f"\nProcessing {fname} -> {target_table} (Size: {fsize:,} bytes)...")
    
    with conn.cursor() as cur:
        # Check idempotency in manifest
        if not force:
            cur.execute("""
                SELECT load_id, loaded_at, row_count 
                FROM bronze.load_manifest 
                WHERE file_sha256 = %s AND status = 'SUCCESS'
                ORDER BY loaded_at DESC LIMIT 1
            """, (fhash,))
            prior_load = cur.fetchone()
            
            if prior_load:
                print(f"  [IDEMPOTENT SKIP] File already loaded in load_id={prior_load[0]} at {prior_load[1]} ({prior_load[2]:,} rows).")
                return prior_load[2], 0.0, True

        # Truncate before load to ensure exact idempotency for clean reloads
        cur.execute(f"TRUNCATE TABLE {target_table} RESTART IDENTITY;")

        # Read CSV columns
        if filepath.endswith(".csv"):
            df_iter = pd.read_csv(filepath, dtype=str, keep_default_na=False, chunksize=50000)
        else:
            df_iter = [pd.read_excel(filepath, dtype=str, keep_default_na=False)]

        total_rows = 0
        
        # Get target table business columns (excluding technical audit columns)
        cur.execute(f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = '{target_table.split('.')[0]}' 
              AND table_name = '{target_table.split('.')[1]}'
              AND column_name NOT IN ('_row_id', '_loaded_at', '_source_file')
            ORDER BY ordinal_position
        """)
        db_cols = [r[0] for r in cur.fetchall()]
        
        cols_clause = ", ".join(f'"{c}"' for c in db_cols) + ', "_source_file"'
        
        with cur.copy(f"COPY {target_table} ({cols_clause}) FROM STDIN") as copy:
            for chunk in df_iter:
                col_map = {str(c).lower(): c for c in chunk.columns}
                aligned_data = {}
                for db_col in db_cols:
                    src_col = col_map.get(db_col.lower())
                    if src_col is not None:
                        aligned_data[db_col] = chunk[src_col]
                    else:
                        aligned_data[db_col] = ""
                aligned_data["_source_file"] = fname
                aligned_df = pd.DataFrame(aligned_data)
                
                for row in aligned_df.itertuples(index=False, name=None):
                    cleaned_row = tuple(
                        None if (val is None or str(val).strip() in ("", "\\N", "NULL"))
                        else str(val).replace('\t', ' ').replace('\n', ' ').replace('\r', ' ')
                        for val in row
                    )
                    copy.write_row(cleaned_row)
                    total_rows += 1

        elapsed = time.time() - start_time
        
        # Record into manifest
        cur.execute("""
            INSERT INTO bronze.load_manifest 
            (file_name, file_path, file_size_bytes, file_sha256, target_table, row_count, status, execution_time_seconds)
            VALUES (%s, %s, %s, %s, %s, %s, 'SUCCESS', %s)
        """, (fname, filepath, fsize, fhash, target_table, total_rows, elapsed))
        
        conn.commit()
        print(f"  [SUCCESS] Ingested {total_rows:,} rows in {elapsed:.2f}s ({total_rows/max(elapsed, 0.001):,.0f} rows/s).")
        return total_rows, elapsed, False

def publish_metrics(metrics_data):
    try:
        registry = CollectorRegistry()
        g_rows = Gauge('dwh_bronze_rows_loaded_total', 'Total rows loaded into Bronze table', ['table'], registry=registry)
        g_time = Gauge('dwh_bronze_load_duration_seconds', 'Ingestion duration in seconds', ['table'], registry=registry)
        g_status = Gauge('dwh_bronze_load_status', '1 if load successful, 0 otherwise', ['table'], registry=registry)

        for table, m in metrics_data.items():
            g_rows.labels(table=table).set(m['rows'])
            g_time.labels(table=table).set(m['time'])
            g_status.labels(table=table).set(1 if m['success'] else 0)

        push_to_gateway(PUSHGATEWAY_URL, job='bronze_loader', registry=registry)
        print("\nPrometheus ingestion metrics successfully pushed to Pushgateway.")
    except Exception as e:
        print(f"\n[WARNING] Could not push metrics to Pushgateway: {e}")

def main():
    print("=" * 80)
    print("PHARMA DWH: BRONZE LAYER HIGH-PERFORMANCE INGESTION")
    print("=" * 80)

    try:
        conn = psycopg.connect(CONN_STR)
    except Exception as e:
        print(f"ERROR: Could not connect to PostgreSQL: {e}")
        sys.exit(1)

    metrics_data = {}

    force_reload = "--force" in sys.argv
    for fname, target_table in FILE_TABLE_MAP.items():
        fpath = os.path.join(DATA_DIR, fname)
        if not os.path.exists(fpath):
            print(f"ERROR: Source file {fpath} does not exist!")
            continue
        try:
            rows, elapsed, was_skipped = load_file_to_bronze(conn, fpath, target_table, force=force_reload)
            metrics_data[target_table] = {"rows": rows, "time": elapsed, "success": True}
        except Exception as e:
            print(f"  [FAIL] Failed loading {fname}: {e}")
            conn.rollback()
            metrics_data[target_table] = {"rows": 0, "time": 0.0, "success": False}

    conn.close()
    publish_metrics(metrics_data)
    print("\n" + "=" * 80)
    print("BRONZE INGESTION COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    main()
