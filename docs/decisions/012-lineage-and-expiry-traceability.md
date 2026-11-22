# ADR-012: Upstream Lineage and Expiry Date Authority

- **Status**: ACCEPTED
- **Date**: 2026-11-22
- **Context**: 100% of sales resolve to valid warehouse lots and production batches; DaysToExpiryAtSale matches BatchExpiryDate - SalesDate exactly.
- **Decision**: BatchExpiryDate from upstream batch/lot lineage is authoritative; store DaysToExpiryAtSale as point-of-sale lead time.
- **Consequences**: Codified in dbt models and verified in Stage 1 test suite.
- **Confidence**: HIGH
