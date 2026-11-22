import psycopg
conn = psycopg.connect("host=postgres port=5432 dbname=dwh user=pharma_admin password=pharma_secret_pw")
cur = conn.cursor()
for schema in ('silver', 'gold', 'obs'):
    cur.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema='{schema}' ORDER BY 1;")
    rows = cur.fetchall()
    print(f"\n--- {schema} ---")
    for r in rows:
        cur2 = conn.cursor()
        cur2.execute(f"SELECT COUNT(*) FROM {schema}.{r[0]}")
        cnt = cur2.fetchone()[0]
        print(f"  {r[0]}: {cnt:,}")
conn.close()
