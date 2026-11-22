# ADR-008: Authoritative Measure for Customer Returns

- **Status**: ACCEPTED
- **Date**: 2026-11-22
- **Context**: ReturnedQuantityPacks is never greater than QuantitySoldPacks and strictly aligns with ReturnFlag='Y'.
- **Decision**: Store ReturnedQuantityPacks as the primary additive return metric in Fact_PharmacySales; keep ReturnFlag in junk dimension.
- **Consequences**: Codified in dbt models and verified in Stage 1 test suite.
- **Confidence**: HIGH
