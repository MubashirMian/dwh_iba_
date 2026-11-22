-- dashboard: Stockout & Expiry Exposure; widget: q2_stockout_expiry_exposure
WITH top_velocity_medicines AS (
    SELECT m.MedicineID, m.GenericName, m.TherapeuticClass,
           SUM(s.QuantitySoldPacks) AS TotalUnitsSold,
           DENSE_RANK() OVER (PARTITION BY m.TherapeuticClass ORDER BY SUM(s.QuantitySoldPacks) DESC) AS VelocityRank
    FROM fact_pharm_sales s
    JOIN dim_medicine m ON s.MedicineSK = m.MedicineSK
    GROUP BY m.MedicineID, m.GenericName, m.TherapeuticClass
),
latest_inventory_snapshot AS (
    SELECT inv.WarehouseSK, m.MedicineID, inv.WarehouseLotID,
           w.WarehouseName, w.Region,
           inv.AvailableQuantityPacks,
           inv.DaysToExpiry,
           inv.StockoutFlag,
           inv.FEFOComplianceFlag,
           CASE WHEN inv.DaysToExpiry <= 30 THEN 'Critical (<30d)'
                WHEN inv.DaysToExpiry <= 60 THEN 'High Risk (31-60d)'
                WHEN inv.DaysToExpiry <= 90 THEN 'Moderate Risk (61-90d)'
                ELSE 'Healthy (>90d)' END AS ExpiryRiskCategory
    FROM fact_inventory inv
    JOIN dim_warehouse w ON inv.WarehouseSK = w.WarehouseSK
    JOIN dim_medicine m ON inv.MedicineSK = m.MedicineSK
    WHERE inv.DateKey = (SELECT MAX(DateKey) FROM fact_inventory)
)
SELECT tvm.TherapeuticClass,
       tvm.GenericName AS TopMedicine,
       tvm.TotalUnitsSold,
       lis.WarehouseName,
       lis.WarehouseLotID,
       lis.AvailableQuantityPacks,
       lis.DaysToExpiry,
       lis.ExpiryRiskCategory,
       lis.StockoutFlag,
       lis.FEFOComplianceFlag
FROM top_velocity_medicines tvm
JOIN latest_inventory_snapshot lis ON tvm.MedicineID = lis.MedicineID
WHERE tvm.VelocityRank <= 3
  AND (lis.DaysToExpiry <= 90 OR lis.StockoutFlag = 1 OR lis.FEFOComplianceFlag = 0)
ORDER BY tvm.TherapeuticClass, lis.DaysToExpiry ASC;