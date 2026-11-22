-- dim_date.sql


WITH date_spine AS (
    SELECT generate_series(DATE '2023-01-01', DATE '2026-12-31', INTERVAL '1 day')::DATE AS full_date
)
SELECT
    TO_CHAR(full_date, 'YYYYMMDD')::INT AS date_key,
    full_date,
    EXTRACT(YEAR FROM full_date)::SMALLINT AS calendar_year,
    EXTRACT(QUARTER FROM full_date)::SMALLINT AS calendar_quarter,
    TO_CHAR(full_date, 'Month') AS month_name,
    EXTRACT(MONTH FROM full_date)::SMALLINT AS month_number,
    EXTRACT(DAY FROM full_date)::SMALLINT AS day_of_month,
    TO_CHAR(full_date, 'Day') AS day_of_week_name,
    CASE WHEN EXTRACT(ISODOW FROM full_date) IN (6, 7) THEN TRUE ELSE FALSE END AS is_weekend_flag
FROM date_spine