-- dim_facility.sql
{{ config(materialized='table') }}

WITH all_facilities AS (
    -- Commercial Pharmacies from Sales
    SELECT DISTINCT
        pharmacy_id AS facility_id,
        pharmacy_name AS facility_name,
        pharmacy_type AS facility_type,
        city,
        state
    FROM {{ ref('silver_pharmacy_sales') }}
    
    UNION
    
    -- Hospital Facilities from Demand
    SELECT DISTINCT
        hospital_id AS facility_id,
        hospital_name AS facility_name,
        hospital_type AS facility_type,
        city,
        state
    FROM {{ ref('silver_hospital_demand') }}
)
SELECT
    ROW_NUMBER() OVER (ORDER BY facility_id) AS facility_sk,
    facility_id,
    facility_name,
    facility_type,
    city,
    state,
    CASE 
        WHEN state IN ('NY', 'PA', 'MA', 'NJ') THEN 'Northeast'
        WHEN state IN ('IL', 'OH', 'MI', 'IN') THEN 'Midwest'
        WHEN state IN ('TX', 'FL', 'GA', 'NC') THEN 'South'
        ELSE 'West'
    END AS region
FROM all_facilities
