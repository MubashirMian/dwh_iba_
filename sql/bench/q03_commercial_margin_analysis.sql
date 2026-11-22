-- dashboard: Commercial Profitability; widget: q03_commercial_margin_analysis
SELECT f.facility_type AS SalesChannel,
       m.therapeutic_class,
       COUNT(DISTINCT s.sales_transaction_id) AS TotalOrders,
       SUM(s.quantity_sold_packs) AS TotalPacksSold,
       SUM(s.gross_sales_amount_usd) AS GrossSalesUSD,
       SUM(s.discount_amount_usd) AS TotalDiscountsUSD,
       ROUND(SUM(s.discount_amount_usd) / NULLIF(SUM(s.gross_sales_amount_usd), 0) * 100, 2) AS DiscountPenetrationPct,
       SUM(s.net_sales_amount_usd) AS NetSalesUSD,
       SUM(s.cost_of_goods_sold_usd) AS TotalCOGS_USD,
       SUM(s.gross_margin_usd) AS GrossMarginUSD,
       ROUND(SUM(s.gross_margin_usd) / NULLIF(SUM(s.net_sales_amount_usd), 0) * 100, 2) AS GrossMarginPct,
       ROUND(SUM(s.returned_quantity_packs)::NUMERIC / NULLIF(SUM(s.quantity_sold_packs), 0) * 100, 2) AS ReturnRatePct,
       ROUND(SUM(s.days_to_expiry_at_sale * s.quantity_sold_packs)::NUMERIC / NULLIF(SUM(s.quantity_sold_packs), 0), 1) AS PackWeightedAvgDaysToExpiry
FROM gold.fact_pharm_sales s
JOIN gold.dim_medicine m ON s.medicine_sk = m.medicine_sk
JOIN gold.dim_facility f ON s.facility_sk = f.facility_sk
GROUP BY f.facility_type, m.therapeutic_class
ORDER BY GrossMarginUSD DESC;
