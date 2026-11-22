-- silver_master_data.sql


SELECT
    
    NULLIF(NULLIF(NULLIF(TRIM("medicineid"), ''), '\N'), 'NULL')
 AS medicine_id,
    
    NULLIF(NULLIF(NULLIF(TRIM("internalsku"), ''), '\N'), 'NULL')
 AS internal_sku,
    
    NULLIF(NULLIF(NULLIF(TRIM("gtin14"), ''), '\N'), 'NULL')
 AS gtin14,
    
    NULLIF(NULLIF(NULLIF(TRIM("genericname"), ''), '\N'), 'NULL')
 AS generic_name,
    
    NULLIF(NULLIF(NULLIF(TRIM("fictionalbrandname"), ''), '\N'), 'NULL')
 AS brand_name,
    
    NULLIF(NULLIF(NULLIF(TRIM("diseasecategory"), ''), '\N'), 'NULL')
 AS disease_category,
    
    NULLIF(NULLIF(NULLIF(TRIM("icd10category"), ''), '\N'), 'NULL')
 AS icd10_category,
    
    NULLIF(NULLIF(NULLIF(TRIM("atccode"), ''), '\N'), 'NULL')
 AS atc_code,
    
    NULLIF(NULLIF(NULLIF(TRIM("therapeuticclass"), ''), '\N'), 'NULL')
 AS therapeutic_class,
    
    NULLIF(NULLIF(NULLIF(TRIM("dosageform"), ''), '\N'), 'NULL')
 AS dosage_form,
    
    NULLIF(NULLIF(NULLIF(TRIM("strength"), ''), '\N'), 'NULL')
 AS strength,
    
    NULLIF(NULLIF(NULLIF(TRIM("routeofadministration"), ''), '\N'), 'NULL')
 AS route_of_administration,
    
    NULLIF(NULLIF(NULLIF(TRIM("packsize"), ''), '\N'), 'NULL')
::INT AS pack_size,
    
    NULLIF(NULLIF(NULLIF(TRIM("baseunitofmeasure"), ''), '\N'), 'NULL')
 AS base_uom,
    
    NULLIF(NULLIF(NULLIF(TRIM("prescriptionclass"), ''), '\N'), 'NULL')
 AS prescription_class,
    
    NULLIF(NULLIF(NULLIF(TRIM("controlledmedicineflag"), ''), '\N'), 'NULL')
 AS controlled_medicine_flag,
    
    NULLIF(NULLIF(NULLIF(TRIM("coldchainflag"), ''), '\N'), 'NULL')
 AS cold_chain_flag,
    
    NULLIF(NULLIF(NULLIF(TRIM("storagemintempc"), ''), '\N'), 'NULL')
::NUMERIC(6, 2) AS storage_min_temp_c,
    
    NULLIF(NULLIF(NULLIF(TRIM("storagemaxtempc"), ''), '\N'), 'NULL')
::NUMERIC(6, 2) AS storage_max_temp_c,
    
    NULLIF(NULLIF(NULLIF(TRIM("maxhumiditypct"), ''), '\N'), 'NULL')
::NUMERIC(6, 2) AS max_humidity_pct,
    
    NULLIF(NULLIF(NULLIF(TRIM("shelflifemonths"), ''), '\N'), 'NULL')
::INT AS shelf_life_months,
    
    NULLIF(NULLIF(NULLIF(TRIM("minimumremainingshelflifedays"), ''), '\N'), 'NULL')
::INT AS min_remaining_shelf_life_days,
    
    NULLIF(NULLIF(NULLIF(TRIM("primarysupplierid"), ''), '\N'), 'NULL')
 AS primary_supplier_id,
    
    NULLIF(NULLIF(NULLIF(TRIM("primaryplantid"), ''), '\N'), 'NULL')
 AS primary_plant_id,
    
    NULLIF(NULLIF(NULLIF(TRIM("manufacturingleadtimedays"), ''), '\N'), 'NULL')
::INT AS manufacturing_lead_time_days,
    
    NULLIF(NULLIF(NULLIF(TRIM("standardbatchsizepacks"), ''), '\N'), 'NULL')
::INT AS standard_batch_size_packs,
    
    NULLIF(NULLIF(NULLIF(TRIM("safetystockdays"), ''), '\N'), 'NULL')
::INT AS safety_stock_days,
    
    NULLIF(NULLIF(NULLIF(TRIM("reorderreviewcycledays"), ''), '\N'), 'NULL')
::INT AS reorder_review_cycle_days,
    
    NULLIF(NULLIF(NULLIF(TRIM("unitmanufacturingcostusd"), ''), '\N'), 'NULL')
::NUMERIC(12, 2) AS unit_manufacturing_cost_usd,
    
    NULLIF(NULLIF(NULLIF(TRIM("wholesalepriceusd"), ''), '\N'), 'NULL')
::NUMERIC(12, 2) AS wholesale_price_usd,
    
    NULLIF(NULLIF(NULLIF(TRIM("recommendedretailpriceusd"), ''), '\N'), 'NULL')
::NUMERIC(12, 2) AS recommended_retail_price_usd,
    
    NULLIF(NULLIF(NULLIF(TRIM("productstatus"), ''), '\N'), 'NULL')
 AS product_status,
    
    NULLIF(NULLIF(NULLIF(TRIM("effectivefromdate"), ''), '\N'), 'NULL')
::DATE AS effective_from_date,
    
    NULLIF(NULLIF(NULLIF(TRIM("sourcesystem"), ''), '\N'), 'NULL')
 AS source_system,
    _loaded_at,
    _row_id
FROM bronze.master_data
WHERE 
    NULLIF(NULLIF(NULLIF(TRIM("medicineid"), ''), '\N'), 'NULL')
 IS NOT NULL