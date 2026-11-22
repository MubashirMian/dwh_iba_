# Analytical Query Verification Report (Q1 - Q3)

Generated automatically by `scripts/verify_sdi.py`.

## 1. As-Written Query Execution Anomalies
1. **Q1 (Sales vs Demand)**:
   - **Error**: Binder Error: `Ambiguous reference to column MonthNumber`.
   - **Resolution**: Explicitly qualified column in CTE alias and SELECT list (`COALESCE(s.MonthNumber, dem.MonthNumber) AS MonthNumber`).
2. **Q2 (Stockout & Expiry Exposure)**:
   - **Vulnerability**: Joining sales velocity and warehouse inventory on `MedicineSK` breaks under SCD Type 2 when multiple versions exist.
   - **Resolution**: Cross-fact grain joined on natural key `MedicineID`.
3. **Q3 (Commercial Profitability)**:
   - **Improvement**: Simple arithmetic average of `DaysToExpiryAtSale` distorts volume. Fixed to **pack-weighted average** (`SUM(DaysToExpiryAtSale * QuantitySold) / SUM(QuantitySold)`).

## 2. Reconciliations to Raw Data
- **Q1' Units Sold**: Matches `05_pharmacy_sales_data.csv` sum: 594,774 packs.
- **Q1' Hospital Consumed**: Matches `06_hospital_demand_data.csv` sum: 5,649,506 packs.
- **Q3' Net Sales**: Reconciles exactly to 5,971,058.76 USD.
