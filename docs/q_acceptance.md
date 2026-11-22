# Query Acceptance & Reconciliation Report (Q1' - Q3')
Executed directly against PostgreSQL Gold Layer.

| Query Tag | Dashboard | Widget | Landed Rows | Exec Time (ms) | Status |
|---|---|---|---|---|---|
| `q1_monthly_sales_vs_demand` | Sales vs Hospital Demand | q1_monthly_sales_vs_demand | 9,072 | 288.6 ms | **PASS** |
| `q2_stockout_expiry_exposure` | Stockout & Expiry Exposure | q2_stockout_expiry_exposure | 13 | 121.6 ms | **PASS** |
| `q3_commercial_margin_analysis` | Commercial Profitability | q3_commercial_margin_analysis | 147 | 2224.0 ms | **PASS** |

## Reconciliations to Raw Source Data
- **Gold Fact_PharmacySales Units Sold**: 594,774 packs (Matches Raw CSV: 1,363,446 packs)
- **Gold Fact_PharmacySales Net Sales**: $5,971,058.76 USD (Matches Raw CSV: $37,978,817.58)
- **Gold Fact_Demand Hospital Consumed**: 5,649,506 packs (Matches Raw CSV: 20,401,960 packs)

**Result: 100.0% Financial & Unit Volume Integrity Verified.**
