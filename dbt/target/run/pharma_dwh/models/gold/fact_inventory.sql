
  
    

  create  table "dwh"."gold"."fact_inventory__dbt_tmp"
  
  
    as
  
  (
    -- fact_inventory.sql


SELECT
    inv.inventory_snapshot_id,
    d.date_key,
    m.medicine_sk,
    w.warehouse_sk,
    inv.warehouse_lot_id,
    inv.storage_zone_id,
    inv.production_batch_id,
    inv.batch_expiry_date,
    inv.days_to_expiry,
    inv.available_quantity_packs,
    inv.reserved_quantity_packs,
    inv.opening_quantity_packs,
    inv.received_quantity_packs,
    inv.shipped_quantity_packs,
    inv.closing_quantity_packs,
    inv.stockout_flag,
    inv.near_expiry_flag,
    inv.fefo_compliance_flag
FROM "dwh"."silver"."silver_warehouse_inventory" inv
JOIN "dwh"."gold"."dim_date" d 
  ON d.date_key = TO_CHAR(inv.snapshot_date, 'YYYYMMDD')::INT
JOIN "dwh"."gold"."dim_medicine" m 
  ON inv.medicine_id = m.medicine_id 
 AND inv.snapshot_date >= m.effective_start_date 
 AND inv.snapshot_date < m.effective_end_date
JOIN "dwh"."gold"."dim_warehouse" w 
  ON inv.warehouse_id = w.warehouse_id
  );
  