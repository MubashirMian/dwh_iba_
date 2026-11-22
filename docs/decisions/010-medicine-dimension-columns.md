# ADR-010: Enrichment of DimMedicine Attributes

- **Status**: ACCEPTED
- **Date**: 2026-11-22
- **Context**: Master data contains valid wholesale prices, shelf life, and storage conditions.
- **Decision**: Carry WholesalePriceUSD, StorageMinTempC, StorageMaxTempC, and ShelfLifeMonths into DimMedicine.
- **Consequences**: Codified in dbt models and verified in Stage 1 test suite.
- **Confidence**: HIGH
