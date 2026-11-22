# ADR-005: Sales Channel and Hospital Dispensary Disambiguation

- **Status**: ACCEPTED
- **Date**: 2026-11-22
- **Context**: 05_pharmacy_sales_data contains 50,305 hospital pharmacy sales with HospitalID populated alongside commercial physical and e-commerce transactions.
- **Decision**: Model DimChannel with 2 commercial transport channels while using DimFacility.FacilityType to isolate hospital pharmacy dispensaries, preventing double-counting in Q1.
- **Consequences**: Codified in dbt models and verified in Stage 1 test suite.
- **Confidence**: HIGH
