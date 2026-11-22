# Workbook Change List for v01

Precise cell-by-cell and sheet-level modifications to apply to `DAWH_DWH_Pharma_ColdChain_Sales_Demand-01.xlsx`:

1. **Sheet `Business.Req.XRay`**:
   - `C7`: Clarify case studies with professional architectural citations.
   - `C10`: Add annotation to OTIF metric: `(Note: OTIF logistics tracking introduced in Phase 3)`.
2. **Sheet `OLTP.XRay`**:
   - `C2`: Replace colloquial text with formal business objective: `Provide synchronized analytical visibility across commercial sales, clinical demand, and warehouse inventory positions to prevent cold-chain stockouts and expiry waste.`
   - `C3`: Ensure all 4 SDI sources are listed: `01_master_data.csv, 04_warehouse_data.csv, 05_pharmacy_sales_data.csv, 06_hospital_demand_data.csv`.
3. **Sheet `Star.Schema`**:
   - Replace SQL Q1 with `sql/verification/q1_fixed.sql` (fixes ambiguous `MonthNumber`).
   - Replace SQL Q2 with `sql/verification/q2_fixed.sql` (joins on natural key `MedicineID` to eliminate SCD2 version splitting).
   - Replace SQL Q3 with `sql/verification/q3_fixed.sql` (uses pack-weighted average for remaining shelf life).
   - Add new "Result evidence" block displaying row counts and sample results.
4. **Add Sheet `Changelog`**:
   - Document every change, corresponding finding ID, before text, and after text.
