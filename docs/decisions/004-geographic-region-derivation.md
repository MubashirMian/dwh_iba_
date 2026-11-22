# ADR-004: Conformed 4-Region Geographic Derivation from State

- **Status**: ACCEPTED
- **Date**: 2026-11-22
- **Context**: Source datasets contain US state codes across facilities and warehouses but lack a native Region column.
- **Decision**: Derive 4 conformed US regions (Northeast, Midwest, South, West) via centralized dbt mapping with 100% test coverage.
- **Consequences**: Codified in dbt models and verified in Stage 1 test suite.
- **Confidence**: HIGH
