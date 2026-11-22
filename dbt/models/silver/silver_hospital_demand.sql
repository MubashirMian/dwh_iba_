-- silver_hospital_demand.sql
{{ config(materialized='view') }}

SELECT
    {{ clean_null('"hospitaldemandrecordid"') }} AS demand_record_id,
    {{ clean_null('"demandmonth"') }}::DATE AS demand_month,
    {{ clean_null('"hospitalid"') }} AS hospital_id,
    {{ clean_null('"hospitalgln"') }} AS hospital_gln,
    {{ clean_null('"hospitalname"') }} AS hospital_name,
    {{ clean_null('"hospitaltype"') }} AS hospital_type,
    {{ clean_null('"hospitalpharmacyid"') }} AS hospital_pharmacy_id,
    {{ clean_null('"city"') }} AS city,
    {{ clean_null('"state"') }} AS state,
    {{ clean_null('"countrycode"') }} AS country_code,
    {{ clean_null('"licensedbeds"') }}::INT AS licensed_beds,
    {{ clean_null('"icubeds"') }}::INT AS icu_beds,
    {{ clean_null('"averageoccupancyratepct"') }}::NUMERIC(6, 2) AS average_occupancy_rate_pct,
    {{ clean_null('"traumalevel"') }} AS trauma_level,
    {{ clean_null('"medicineid"') }} AS medicine_id,
    {{ clean_null('"gtin14"') }} AS gtin14,
    {{ clean_null('"genericname"') }} AS generic_name,
    {{ clean_null('"diseasecategory"') }} AS disease_category,
    {{ clean_null('"forecastdemandpacks"') }}::INT AS forecast_demand_packs,
    {{ clean_null('"requestedquantitypacks"') }}::INT AS requested_quantity_packs,
    {{ clean_null('"approvedquantitypacks"') }}::INT AS approved_quantity_packs,
    {{ clean_null('"receivedquantitypacks"') }}::INT AS received_quantity_packs,
    {{ clean_null('"consumedquantitypacks"') }}::INT AS consumed_quantity_packs,
    {{ clean_null('"unfulfilleddemandpacks"') }}::INT AS unfulfilled_demand_packs,
    {{ clean_null('"stockoutdays"') }}::INT AS stockout_days,
    {{ clean_null('"medicationrequeststatus"') }} AS request_status,
    _loaded_at,
    _row_id
FROM bronze.hospital_demand_data
WHERE {{ clean_null('"hospitaldemandrecordid"') }} IS NOT NULL
