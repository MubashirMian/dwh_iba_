-- silver_warehouse_inventory.sql
{{ config(materialized='view') }}

SELECT
    {{ clean_null('"inventorysnapshotid"') }} AS inventory_snapshot_id,
    {{ clean_null('"snapshotdate"') }}::DATE AS snapshot_date,
    {{ clean_null('"warehouselotid"') }} AS warehouse_lot_id,
    {{ clean_null('"warehouseid"') }} AS warehouse_id,
    {{ clean_null('"warehousegln"') }} AS warehouse_gln,
    {{ clean_null('"warehousename"') }} AS warehouse_name,
    {{ clean_null('"storagezoneid"') }} AS storage_zone_id,
    {{ clean_null('"productionbatchid"') }} AS production_batch_id,
    {{ clean_null('"medicineid"') }} AS medicine_id,
    {{ clean_null('"gtin14"') }} AS gtin14,
    {{ clean_null('"batchexpirydate"') }}::DATE AS batch_expiry_date,
    {{ clean_null('"daystoexpiry"') }}::INT AS days_to_expiry,
    {{ clean_null('"inventorystatus"') }} AS inventory_status,
    {{ clean_null('"availablequantitypacks"') }}::INT AS available_quantity_packs,
    {{ clean_null('"reservedquantitypacks"') }}::INT AS reserved_quantity_packs,
    {{ clean_null('"openingquantitypacks"') }}::INT AS opening_quantity_packs,
    {{ clean_null('"receivedquantitypacks"') }}::INT AS received_quantity_packs,
    {{ clean_null('"shippedquantitypacks"') }}::INT AS shipped_quantity_packs,
    {{ clean_null('"closingquantitypacks"') }}::INT AS closing_quantity_packs,
    CASE WHEN {{ clean_null('"stockoutflag"') }} = 'Y' THEN 1 ELSE 0 END AS stockout_flag,
    CASE WHEN {{ clean_null('"nearexpiryflag"') }} = 'Y' THEN 1 ELSE 0 END AS near_expiry_flag,
    CASE WHEN {{ clean_null('"fefocomplianceflag"') }} = 'Y' THEN 1 ELSE 0 END AS fefo_compliance_flag,
    _loaded_at,
    _row_id
FROM bronze.warehouse_data
WHERE {{ clean_null('"inventorysnapshotid"') }} IS NOT NULL
