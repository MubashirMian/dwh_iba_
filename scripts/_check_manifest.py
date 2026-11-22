import psycopg
conn = psycopg.connect("host=postgres port=5432 dbname=dwh user=pharma_admin password=pharma_secret_pw")
cur = conn.cursor()
cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_schema='bronze' AND table_name='load_manifest' ORDER BY ordinal_position;")
print("--- bronze.load_manifest columns ---")
for r in cur.fetchall():
    print(f"  {r[0]} : {r[1]}")
cur.execute("SELECT * FROM bronze.load_manifest LIMIT 2;")
cols = [d[0] for d in cur.description]
print(f"\nColumns: {cols}")
for r in cur.fetchall():
    print(f"  {r}")
conn.close()
