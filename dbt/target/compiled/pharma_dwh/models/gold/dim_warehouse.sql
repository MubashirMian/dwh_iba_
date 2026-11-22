-- dim_warehouse.sql


SELECT
    ROW_NUMBER() OVER (ORDER BY warehouse_id) AS warehouse_sk,
    warehouse_id,
    warehouse_name,
    warehouse_gln,
    'West' AS region
FROM (
    SELECT DISTINCT
        warehouse_id,
        warehouse_name,
        warehouse_gln
    FROM "dwh"."silver"."silver_warehouse_inventory"
) sub