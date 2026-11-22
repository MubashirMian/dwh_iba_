# Sales & Demand Intelligence (SDI) Metric Dictionary

## Core Commercial Metrics
| Metric Name | Business Definition | Mathematical Formula | Storage Grain | Source Table |
|---|---|---|---|---|
| **CommercialUnitsSold** | Total number of medicine packs sold across commercial pharmacies | `SUM(quantity_sold_packs)` | Transaction | `gold.fact_pharm_sales` |
| **GrossSalesUSD** | Total pre-discount sales revenue | `SUM(gross_sales_amount_usd)` | Transaction | `gold.fact_pharm_sales` |
| **DiscountAmountUSD** | Total monetary discounts applied to commercial sales | `SUM(discount_amount_usd)` | Transaction | `gold.fact_pharm_sales` |
| **DiscountPenetrationPct** | Percentage of gross revenue granted as discount | `(DiscountUSD / GrossSalesUSD) * 100` | Aggregated | Derived |
| **NetSalesUSD** | Authoritative commercial top-line recognized revenue | `SUM(net_sales_amount_usd)` | Transaction | `gold.fact_pharm_sales` |
| **CostOfGoodsSoldUSD** | Direct manufacturing and acquisition cost of sold units | `SUM(cost_of_goods_sold_usd)` | Transaction | `gold.fact_pharm_sales` |
| **GrossMarginUSD** | Financial gross profit generated after COGS | `NetSalesUSD - CostOfGoodsSoldUSD` | Transaction | `gold.fact_pharm_sales` |
| **GrossMarginPct** | Profitability ratio of commercial sales | `(GrossMarginUSD / NetSalesUSD) * 100` | Aggregated | Derived |
| **ReturnRatePct** | Volume percentage of sold packs returned by customers | `(SUM(returned_quantity_packs) / SUM(quantity_sold_packs)) * 100` | Aggregated | Derived |
| **PackWeightedAvgDaysToExpiry** | Shelf-life remaining at point of sale, weighted by volume | `SUM(DaysToExpiryAtSale * QuantitySold) / SUM(QuantitySold)` | Aggregated | Derived |

## Clinical & Demand Fulfillment Metrics
| Metric Name | Business Definition | Mathematical Formula | Storage Grain | Source Table |
|---|---|---|---|---|
| **HospitalRequestedPacks** | Medicine volume requested by hospital dispensaries | `SUM(requested_quantity_packs)` | Facility-Month | `gold.fact_demand` |
| **HospitalConsumedPacks** | Medicine volume consumed in clinical treatments | `SUM(consumed_quantity_packs)` | Facility-Month | `gold.fact_demand` |
| **HospitalUnfulfilledPacks**| Volume of unfulfilled hospital requests (stockouts/shortages) | `SUM(unfulfilled_demand_packs)` | Facility-Month | `gold.fact_demand` |
| **HospitalFillRatePct** | Clinical fulfillment service level | `(HospitalConsumedPacks / HospitalRequestedPacks) * 100` | Aggregated | Derived |
| **StockoutDays** | Total days a specific SKU was out of stock at hospital pharmacy | `SUM(stockout_days)` | Facility-Month | `gold.fact_demand` |

## Warehouse & Inventory Metrics
| Metric Name | Business Definition | Mathematical Formula | Storage Grain | Source Table |
|---|---|---|---|---|
| **AvailableQuantityPacks** | Unreserved stock available for picking and dispatch | `SUM(available_quantity_packs)` | Lot-Daily | `gold.fact_inventory` |
| **DaysToExpiry** | Shelf-life remaining as of snapshot date | As recorded at `snapshot_date` | Lot-Daily | `gold.fact_inventory` |
| **FEFOComplianceRatePct** | Percentage of warehouse movements adhering to FEFO | `AVG(fefo_compliance_flag) * 100` | Aggregated | `gold.fact_inventory` |
| **StockoutFlagRate** | Proportion of lots in stockout condition | `AVG(stockout_flag) * 100` | Aggregated | `gold.fact_inventory` |
