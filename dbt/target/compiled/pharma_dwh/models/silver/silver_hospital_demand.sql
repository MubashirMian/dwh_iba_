-- silver_hospital_demand.sql


SELECT
    
    NULLIF(NULLIF(NULLIF(TRIM("hospitaldemandrecordid"), ''), '\N'), 'NULL')
 AS demand_record_id,
    
    NULLIF(NULLIF(NULLIF(TRIM("demandmonth"), ''), '\N'), 'NULL')
::DATE AS demand_month,
    
    NULLIF(NULLIF(NULLIF(TRIM("hospitalid"), ''), '\N'), 'NULL')
 AS hospital_id,
    
    NULLIF(NULLIF(NULLIF(TRIM("hospitalgln"), ''), '\N'), 'NULL')
 AS hospital_gln,
    
    NULLIF(NULLIF(NULLIF(TRIM("hospitalname"), ''), '\N'), 'NULL')
 AS hospital_name,
    
    NULLIF(NULLIF(NULLIF(TRIM("hospitaltype"), ''), '\N'), 'NULL')
 AS hospital_type,
    
    NULLIF(NULLIF(NULLIF(TRIM("hospitalpharmacyid"), ''), '\N'), 'NULL')
 AS hospital_pharmacy_id,
    
    NULLIF(NULLIF(NULLIF(TRIM("city"), ''), '\N'), 'NULL')
 AS city,
    
    NULLIF(NULLIF(NULLIF(TRIM("state"), ''), '\N'), 'NULL')
 AS state,
    
    NULLIF(NULLIF(NULLIF(TRIM("countrycode"), ''), '\N'), 'NULL')
 AS country_code,
    
    NULLIF(NULLIF(NULLIF(TRIM("licensedbeds"), ''), '\N'), 'NULL')
::INT AS licensed_beds,
    
    NULLIF(NULLIF(NULLIF(TRIM("icubeds"), ''), '\N'), 'NULL')
::INT AS icu_beds,
    
    NULLIF(NULLIF(NULLIF(TRIM("averageoccupancyratepct"), ''), '\N'), 'NULL')
::NUMERIC(6, 2) AS average_occupancy_rate_pct,
    
    NULLIF(NULLIF(NULLIF(TRIM("traumalevel"), ''), '\N'), 'NULL')
 AS trauma_level,
    
    NULLIF(NULLIF(NULLIF(TRIM("medicineid"), ''), '\N'), 'NULL')
 AS medicine_id,
    
    NULLIF(NULLIF(NULLIF(TRIM("gtin14"), ''), '\N'), 'NULL')
 AS gtin14,
    
    NULLIF(NULLIF(NULLIF(TRIM("genericname"), ''), '\N'), 'NULL')
 AS generic_name,
    
    NULLIF(NULLIF(NULLIF(TRIM("diseasecategory"), ''), '\N'), 'NULL')
 AS disease_category,
    
    NULLIF(NULLIF(NULLIF(TRIM("forecastdemandpacks"), ''), '\N'), 'NULL')
::INT AS forecast_demand_packs,
    
    NULLIF(NULLIF(NULLIF(TRIM("requestedquantitypacks"), ''), '\N'), 'NULL')
::INT AS requested_quantity_packs,
    
    NULLIF(NULLIF(NULLIF(TRIM("approvedquantitypacks"), ''), '\N'), 'NULL')
::INT AS approved_quantity_packs,
    
    NULLIF(NULLIF(NULLIF(TRIM("receivedquantitypacks"), ''), '\N'), 'NULL')
::INT AS received_quantity_packs,
    
    NULLIF(NULLIF(NULLIF(TRIM("consumedquantitypacks"), ''), '\N'), 'NULL')
::INT AS consumed_quantity_packs,
    
    NULLIF(NULLIF(NULLIF(TRIM("unfulfilleddemandpacks"), ''), '\N'), 'NULL')
::INT AS unfulfilled_demand_packs,
    
    NULLIF(NULLIF(NULLIF(TRIM("stockoutdays"), ''), '\N'), 'NULL')
::INT AS stockout_days,
    
    NULLIF(NULLIF(NULLIF(TRIM("medicationrequeststatus"), ''), '\N'), 'NULL')
 AS request_status,
    _loaded_at,
    _row_id
FROM bronze.hospital_demand_data
WHERE 
    NULLIF(NULLIF(NULLIF(TRIM("hospitaldemandrecordid"), ''), '\N'), 'NULL')
 IS NOT NULL