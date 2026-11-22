# ADR-007: Single Unified DimSalesProfile Junk Dimension

- **Status**: ACCEPTED
- **Date**: 2026-11-22
- **Context**: Low-cardinality transaction flags yield 384 distinct combinations; PromotionCode has manageable distinct values.
- **Decision**: Retain one unified DimSalesProfile junk dimension to optimize storage and join performance.
- **Consequences**: Codified in dbt models and verified in Stage 1 test suite.
- **Confidence**: HIGH
