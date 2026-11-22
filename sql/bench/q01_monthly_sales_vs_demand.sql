-- dashboard: Sales vs Hospital Demand; widget: q01_monthly_sales_vs_demand
WITH monthly_sales AS (
    SELECT d.calendar_year, d.month_name, d.month_number,
           m.medicine_id, m.generic_name, m.disease_category,
           f.region,
           SUM(s.quantity_sold_packs) AS CommercialUnitsSold,
           SUM(s.net_sales_amount_usd) AS CommercialNetSalesUSD
    FROM gold.fact_pharm_sales s
    JOIN gold.dim_date d ON s.date_key = d.date_key
    JOIN gold.dim_medicine m ON s.medicine_sk = m.medicine_sk
    JOIN gold.dim_facility f ON s.facility_sk = f.facility_sk
    GROUP BY d.calendar_year, d.month_name, d.month_number, m.medicine_id, m.generic_name, m.disease_category, f.region
),
monthly_demand AS (
    SELECT d.calendar_year, d.month_name, d.month_number,
           m.medicine_id, m.generic_name, m.disease_category,
           f.region,
           SUM(dem.requested_quantity_packs) AS TotalRequestedPacks,
           SUM(dem.received_quantity_packs) AS TotalReceivedPacks,
           SUM(dem.consumed_quantity_packs) AS TotalConsumedPacks,
           SUM(dem.unfulfilled_demand_packs) AS TotalUnfulfilledPacks
    FROM gold.fact_demand dem
    JOIN gold.dim_date d ON dem.date_key = d.date_key
    JOIN gold.dim_medicine m ON dem.medicine_sk = m.medicine_sk
    JOIN gold.dim_facility f ON dem.facility_sk = f.facility_sk
    GROUP BY d.calendar_year, d.month_name, d.month_number, m.medicine_id, m.generic_name, m.disease_category, f.region
)
SELECT COALESCE(s.calendar_year, dem.calendar_year) AS Year,
       COALESCE(s.month_name, dem.month_name) AS Month,
       COALESCE(s.month_number, dem.month_number) AS MonthNumber,
       COALESCE(s.generic_name, dem.generic_name) AS Medicine,
       COALESCE(s.disease_category, dem.disease_category) AS Disease,
       COALESCE(s.region, dem.region) AS Region,
       COALESCE(s.CommercialUnitsSold, 0) AS UnitsSold_Commercial,
       COALESCE(dem.TotalRequestedPacks, 0) AS Requested_Hospital,
       COALESCE(dem.TotalConsumedPacks, 0) AS Consumed_Hospital,
       COALESCE(dem.TotalUnfulfilledPacks, 0) AS Unfulfilled_Hospital,
       ROUND(COALESCE(dem.TotalConsumedPacks, 0)::NUMERIC / NULLIF(dem.TotalRequestedPacks, 0) * 100, 2) AS HospitalFillRatePct
FROM monthly_sales s
FULL OUTER JOIN monthly_demand dem
  ON s.calendar_year = dem.calendar_year
 AND s.month_number = dem.month_number
 AND s.medicine_id = dem.medicine_id
 AND s.region = dem.region
ORDER BY Year DESC, MonthNumber DESC, Unfulfilled_Hospital DESC;
