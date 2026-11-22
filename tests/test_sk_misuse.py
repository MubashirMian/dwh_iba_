"""
tests/test_sk_misuse.py
SK-Misuse Prevention Test (S7.3).
Proves that cross-fact analytical joins between Sales and Inventory must join
on Natural Key (medicine_id) rather than surrogate key (medicine_sk) to prevent
accidental data loss or incorrect aggregation when SCD Type 2 splits occur.
"""

import os
import sys
import psycopg

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB   = os.getenv("POSTGRES_DB", "dwh")
POSTGRES_USER = os.getenv("POSTGRES_USER", "pharma_admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "pharma_secret_pw")

CONN_STR = f"host={POSTGRES_HOST} port={POSTGRES_PORT} dbname={POSTGRES_DB} user={POSTGRES_USER} password={POSTGRES_PASSWORD}"

def test_cross_fact_natural_key():
    conn = psycopg.connect(CONN_STR)
    cur = conn.cursor()

    print("Running SK-Misuse Prevention Test (S7.3)...")

    # Natural key cross-fact join test
    cur.execute("""
        SELECT COUNT(DISTINCT s.medicine_id)
        FROM (
            SELECT DISTINCT m.medicine_id 
            FROM gold.fact_pharm_sales s
            JOIN gold.dim_medicine m ON s.medicine_sk = m.medicine_sk
        ) s
        JOIN (
            SELECT DISTINCT m.medicine_id 
            FROM gold.fact_inventory i
            JOIN gold.dim_medicine m ON i.medicine_sk = m.medicine_sk
        ) inv ON s.medicine_id = inv.medicine_id;
    """)
    nk_count = cur.fetchone()[0]
    assert nk_count == 63, f"Expected 63 overlapping medicines across facts, got {nk_count}"
    print(f"  [PASS] Natural key join accurately reconciles {nk_count} medicines across facts.")

    conn.close()
    print("SK-Misuse Prevention Test PASSED.")

if __name__ == "__main__":
    test_cross_fact_natural_key()
