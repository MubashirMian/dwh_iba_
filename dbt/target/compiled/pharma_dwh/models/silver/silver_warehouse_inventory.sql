-- silver_warehouse_inventory.sql


SELECT
    
    NULLIF(NULLIF(NULLIF(TRIM("inventorysnapshotid"), ''), '\N'), 'NULL')
 AS inventory_snapshot_id,
    
    NULLIF(NULLIF(NULLIF(TRIM("snapshotdate"), ''), '\N'), 'NULL')
::DATE AS snapshot_date,
    
    NULLIF(NULLIF(NULLIF(TRIM("warehouselotid"), ''), '\N'), 'NULL')
 AS warehouse_lot_id,
    
    NULLIF(NULLIF(NULLIF(TRIM("warehouseid"), ''), '\N'), 'NULL')
 AS warehouse_id,
    
    NULLIF(NULLIF(NULLIF(TRIM("warehousegln"), ''), '\N'), 'NULL')
 AS warehouse_gln,
    
    NULLIF(NULLIF(NULLIF(TRIM("warehousename"), ''), '\N'), 'NULL')
 AS warehouse_name,
    
    NULLIF(NULLIF(NULLIF(TRIM("storagezoneid"), ''), '\N'), 'NULL')
 AS storage_zone_id,
    
    NULLIF(NULLIF(NULLIF(TRIM("productionbatchid"), ''), '\N'), 'NULL')
 AS production_batch_id,
    
    NULLIF(NULLIF(NULLIF(TRIM("medicineid"), ''), '\N'), 'NULL')
 AS medicine_id,
    
    NULLIF(NULLIF(NULLIF(TRIM("gtin14"), ''), '\N'), 'NULL')
 AS gtin14,
    
    NULLIF(NULLIF(NULLIF(TRIM("batchexpirydate"), ''), '\N'), 'NULL')
::DATE AS batch_expiry_date,
    
    NULLIF(NULLIF(NULLIF(TRIM("daystoexpiry"), ''), '\N'), 'NULL')
::INT AS days_to_expiry,
    
    NULLIF(NULLIF(NULLIF(TRIM("inventorystatus"), ''), '\N'), 'NULL')
 AS inventory_status,
    
    NULLIF(NULLIF(NULLIF(TRIM("availablequantitypacks"), ''), '\N'), 'NULL')
::INT AS available_quantity_packs,
    
    NULLIF(NULLIF(NULLIF(TRIM("reservedquantitypacks"), ''), '\N'), 'NULL')
::INT AS reserved_quantity_packs,
    
    NULLIF(NULLIF(NULLIF(TRIM("openingquantitypacks"), ''), '\N'), 'NULL')
::INT AS opening_quantity_packs,
    
    NULLIF(NULLIF(NULLIF(TRIM("receivedquantitypacks"), ''), '\N'), 'NULL')
::INT AS received_quantity_packs,
    
    NULLIF(NULLIF(NULLIF(TRIM("shippedquantitypacks"), ''), '\N'), 'NULL')
::INT AS shipped_quantity_packs,
    
    NULLIF(NULLIF(NULLIF(TRIM("closingquantitypacks"), ''), '\N'), 'NULL')
::INT AS closing_quantity_packs,
    CASE WHEN 
    NULLIF(NULLIF(NULLIF(TRIM("stockoutflag"), ''), '\N'), 'NULL')
 = 'Y' THEN 1 ELSE 0 END AS stockout_flag,
    CASE WHEN 
    NULLIF(NULLIF(NULLIF(TRIM("nearexpiryflag"), ''), '\N'), 'NULL')
 = 'Y' THEN 1 ELSE 0 END AS near_expiry_flag,
    CASE WHEN 
    NULLIF(NULLIF(NULLIF(TRIM("fefocomplianceflag"), ''), '\N'), 'NULL')
 = 'Y' THEN 1 ELSE 0 END AS fefo_compliance_flag,
    _loaded_at,
    _row_id
FROM bronze.warehouse_data
WHERE 
    NULLIF(NULLIF(NULLIF(TRIM("inventorysnapshotid"), ''), '\N'), 'NULL')
 IS NOT NULL