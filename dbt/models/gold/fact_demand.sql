-- fact_demand.sql
{{ config(materialized='table') }}

SELECT
    dem.demand_record_id,
    d.date_key,
    m.medicine_sk,
    f.facility_sk,
    dem.forecast_demand_packs,
    dem.requested_quantity_packs,
    dem.approved_quantity_packs,
    dem.received_quantity_packs,
    dem.consumed_quantity_packs,
    dem.unfulfilled_demand_packs,
    dem.stockout_days,
    dem.request_status
FROM {{ ref('silver_hospital_demand') }} dem
JOIN {{ ref('dim_date') }} d 
  ON d.date_key = TO_CHAR(dem.demand_month, 'YYYYMMDD')::INT
JOIN {{ ref('dim_medicine') }} m 
  ON dem.medicine_id = m.medicine_id 
 AND dem.demand_month >= m.effective_start_date 
 AND dem.demand_month < m.effective_end_date
JOIN {{ ref('dim_facility') }} f 
  ON dem.hospital_pharmacy_id = f.facility_id
