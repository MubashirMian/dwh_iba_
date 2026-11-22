-- dim_medicine.sql


SELECT
    ROW_NUMBER() OVER (ORDER BY medicine_id) AS medicine_sk,
    medicine_id,
    internal_sku,
    gtin14,
    generic_name,
    brand_name,
    disease_category,
    icd10_category,
    atc_code,
    therapeutic_class,
    dosage_form,
    strength,
    wholesale_price_usd,
    recommended_retail_price_usd,
    unit_manufacturing_cost_usd,
    storage_min_temp_c,
    storage_max_temp_c,
    shelf_life_months,
    effective_from_date AS effective_start_date,
    DATE '9999-12-31' AS effective_end_date,
    TRUE AS is_current_flag
FROM "dwh"."silver"."silver_master_data"