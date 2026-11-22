-- dashboard: Commercial Profitability; widget: q3_commercial_margin_analysis
SELECT f.FacilityType AS SalesChannel,
       m.TherapeuticClass,
       COUNT(DISTINCT s.SalesTransactionID) AS TotalOrders,
       SUM(s.QuantitySoldPacks) AS TotalPacksSold,
       SUM(s.GrossSalesAmountUSD) AS GrossSalesUSD,
       SUM(s.DiscountAmountUSD) AS TotalDiscountsUSD,
       ROUND(SUM(s.DiscountAmountUSD) / NULLIF(SUM(s.GrossSalesAmountUSD), 0) * 100, 2) AS DiscountPenetrationPct,
       SUM(s.NetSalesAmountUSD) AS NetSalesUSD,
       SUM(s.CostOfGoodsSoldUSD) AS TotalCOGS_USD,
       SUM(s.GrossMarginUSD) AS GrossMarginUSD,
       ROUND(SUM(s.GrossMarginUSD) / NULLIF(SUM(s.NetSalesAmountUSD), 0) * 100, 2) AS GrossMarginPct,
       ROUND(SUM(s.ReturnedQuantityPacks)::NUMERIC / NULLIF(SUM(s.QuantitySoldPacks), 0) * 100, 2) AS ReturnRatePct,
       ROUND(SUM(s.DaysToExpiryAtSale * s.QuantitySoldPacks)::NUMERIC / NULLIF(SUM(s.QuantitySoldPacks), 0), 1) AS PackWeightedAvgDaysToExpiry
FROM fact_pharm_sales s
JOIN dim_medicine m ON s.MedicineSK = m.MedicineSK
JOIN dim_facility f ON s.FacilitySK = f.FacilitySK
GROUP BY f.FacilityType, m.TherapeuticClass
ORDER BY GrossMarginUSD DESC;