import psycopg
conn = psycopg.connect("host=postgres port=5432 dbname=dwh user=pharma_admin password=pharma_secret_pw")
cur = conn.cursor()
# Check dq schema
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='dq' ORDER BY 1;")
rows = cur.fetchall()
print("--- dq ---")
for r in rows:
    print(f"  {r[0]}")

# Check obs.query_log contents
cur.execute("SELECT query_tag, duration_ms, rows_returned, execution_timestamp FROM obs.query_log ORDER BY execution_timestamp DESC LIMIT 10;")
rows = cur.fetchall()
print("\n--- obs.query_log ---")
for r in rows:
    print(f"  {r}")

conn.close()
