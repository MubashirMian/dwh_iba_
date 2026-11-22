-- dashboard: Sales vs Hospital Demand; widget: q1_monthly_sales_vs_demand
WITH monthly_sales AS (
    SELECT d.CalendarYear, d.MonthName, d.MonthNumber,
           m.MedicineID, m.GenericName, m.DiseaseCategory,
           f.Region,
           SUM(s.QuantitySoldPacks) AS CommercialUnitsSold,
           SUM(s.NetSalesAmountUSD) AS CommercialNetSalesUSD
    FROM fact_pharm_sales s
    JOIN dim_date d ON s.DateKey = d.DateKey
    JOIN dim_medicine m ON s.MedicineSK = m.MedicineSK
    JOIN dim_facility f ON s.FacilitySK = f.FacilitySK
    GROUP BY d.CalendarYear, d.MonthName, d.MonthNumber, m.MedicineID, m.GenericName, m.DiseaseCategory, f.Region
),
monthly_demand AS (
    SELECT d.CalendarYear, d.MonthName, d.MonthNumber,
           m.MedicineID, m.GenericName, m.DiseaseCategory,
           f.Region,
           SUM(dem.RequestedQuantityPacks) AS TotalRequestedPacks,
           SUM(dem.ReceivedQuantityPacks) AS TotalReceivedPacks,
           SUM(dem.ConsumedQuantityPacks) AS TotalConsumedPacks,
           SUM(dem.UnfulfilledDemandPacks) AS TotalUnfulfilledPacks
    FROM fact_demand dem
    JOIN dim_date d ON dem.DateKey = d.DateKey
    JOIN dim_medicine m ON dem.MedicineSK = m.MedicineSK
    JOIN dim_facility f ON dem.FacilitySK = f.FacilitySK
    GROUP BY d.CalendarYear, d.MonthName, d.MonthNumber, m.MedicineID, m.GenericName, m.DiseaseCategory, f.Region
)
SELECT COALESCE(s.CalendarYear, dem.CalendarYear) AS Year,
       COALESCE(s.MonthName, dem.MonthName) AS Month,
       COALESCE(s.MonthNumber, dem.MonthNumber) AS MonthNumber,
       COALESCE(s.GenericName, dem.GenericName) AS Medicine,
       COALESCE(s.DiseaseCategory, dem.DiseaseCategory) AS Disease,
       COALESCE(s.Region, dem.Region) AS Region,
       COALESCE(s.CommercialUnitsSold, 0) AS UnitsSold_Commercial,
       COALESCE(dem.TotalRequestedPacks, 0) AS Requested_Hospital,
       COALESCE(dem.TotalConsumedPacks, 0) AS Consumed_Hospital,
       COALESCE(dem.TotalUnfulfilledPacks, 0) AS Unfulfilled_Hospital,
       ROUND(COALESCE(dem.TotalConsumedPacks, 0)::NUMERIC / NULLIF(dem.TotalRequestedPacks, 0) * 100, 2) AS HospitalFillRatePct
FROM monthly_sales s
FULL OUTER JOIN monthly_demand dem
  ON s.CalendarYear = dem.CalendarYear
 AND s.MonthNumber = dem.MonthNumber
 AND s.MedicineID = dem.MedicineID
 AND s.Region = dem.Region
ORDER BY Year DESC, MonthNumber DESC, Unfulfilled_Hospital DESC;