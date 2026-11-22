-- dashboard: Stockout & Expiry Exposure; widget: q02_stockout_expiry_exposure
WITH top_velocity_medicines AS (
    SELECT m.medicine_id, m.generic_name, m.therapeutic_class,
           SUM(s.quantity_sold_packs) AS TotalUnitsSold,
           DENSE_RANK() OVER (PARTITION BY m.therapeutic_class ORDER BY SUM(s.quantity_sold_packs) DESC) AS VelocityRank
    FROM gold.fact_pharm_sales s
    JOIN gold.dim_medicine m ON s.medicine_sk = m.medicine_sk
    GROUP BY m.medicine_id, m.generic_name, m.therapeutic_class
),
latest_inventory_snapshot AS (
    SELECT inv.warehouse_sk, m.medicine_id, inv.warehouse_lot_id,
           w.warehouse_name, w.region,
           inv.available_quantity_packs,
           inv.days_to_expiry,
           inv.stockout_flag,
           inv.fefo_compliance_flag,
           CASE WHEN inv.days_to_expiry <= 30 THEN 'Critical (<30d)'
                WHEN inv.days_to_expiry <= 60 THEN 'High Risk (31-60d)'
                WHEN inv.days_to_expiry <= 90 THEN 'Moderate Risk (61-90d)'
                ELSE 'Healthy (>90d)' END AS ExpiryRiskCategory
    FROM gold.fact_inventory inv
    JOIN gold.dim_warehouse w ON inv.warehouse_sk = w.warehouse_sk
    JOIN gold.dim_medicine m ON inv.medicine_sk = m.medicine_sk
    WHERE inv.date_key = (SELECT MAX(date_key) FROM gold.fact_inventory)
)
SELECT tvm.therapeutic_class,
       tvm.generic_name AS TopMedicine,
       tvm.TotalUnitsSold,
       lis.warehouse_name,
       lis.warehouse_lot_id,
       lis.available_quantity_packs,
       lis.days_to_expiry,
       lis.ExpiryRiskCategory,
       lis.stockout_flag,
       lis.fefo_compliance_flag
FROM top_velocity_medicines tvm
JOIN latest_inventory_snapshot lis ON tvm.medicine_id = lis.medicine_id
WHERE tvm.VelocityRank <= 3
  AND (lis.days_to_expiry <= 90 OR lis.stockout_flag = 1 OR lis.fefo_compliance_flag = 0)
ORDER BY tvm.therapeutic_class, lis.days_to_expiry ASC;
