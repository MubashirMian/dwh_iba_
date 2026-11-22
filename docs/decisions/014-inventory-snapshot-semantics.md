# ADR-014: Inventory Snapshot Density and DaysToExpiry As-Of Semantics

- **Status**: ACCEPTED
- **Date**: 2026-11-22
- **Context**: Daily warehouse inventory snapshots are 100% dense from 2023 to 2025 with zero missing days; DaysToExpiry degrades strictly by 1 day per calendar day.
- **Decision**: Store DaysToExpiry AS OF SnapshotDate; never recalculate dynamically relative to current wall-clock date.
- **Consequences**: Codified in dbt models and verified in Stage 1 test suite.
- **Confidence**: HIGH
