# ADR-011: Sales Financial Metric Integrity and Derivations

- **Status**: ACCEPTED
- **Date**: 2026-11-22
- **Context**: Zero gross, net, or margin arithmetic errors detected across 500,000 sales transactions.
- **Decision**: Ingest source monetary columns directly; enforce formula consistency tests in dbt test suite.
- **Consequences**: Codified in dbt models and verified in Stage 1 test suite.
- **Confidence**: HIGH
