# ADR-003: SCD2 History Strategy and Controlled Test Fixture

- **Status**: ACCEPTED
- **Date**: 2026-11-22
- **Context**: Base dataset 01_master_data.csv has exactly 63 rows for 63 SKUs with a single effective date.
- **Decision**: Establish SCD Type 2 dbt snapshot infrastructure; use controlled test fixture in Stage 6 to demonstrate point-in-time versioning until full generator runs in Phase 4.
- **Consequences**: Codified in dbt models and verified in Stage 1 test suite.
- **Confidence**: HIGH
