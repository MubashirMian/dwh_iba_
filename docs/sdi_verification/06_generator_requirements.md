# Generator Requirements for Phase 1 Refreshes (R1 & R2)

Based on findings in Stage 1 verification:
1. **SCD Type 2 Injection (H1 Finding)**:
   - Base data has single version per SKU. In refresh R2, generator MUST inject price, cost, and storage range changes for 3-5 SKUs to prove SCD2 validity in production.
2. **Defect Injection (B7 Rule)**:
   - Ingest 0.5% - 1.0% deliberate anomalies (e.g., negative prices, null customer segment) to ensure `dq.rejected_rows` captures real data quality events.
3. **Temporal Expansion (H18 Finding)**:
   - R1 must simulate `2026-01-01` to `2026-03-31`.
   - R2 must simulate `2026-04-01` to `2026-06-30`.
4. **Referential Lineage (H11 Finding)**:
   - Generated sales transactions must preserve valid foreign key lineage back to active warehouse lots and production batches.
