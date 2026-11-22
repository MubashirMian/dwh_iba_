# ADR-015: Base Temporal Span and Simulation Forward Window

- **Status**: ACCEPTED
- **Date**: 2026-11-22
- **Context**: All base source files span exactly 2023-01-01 to 2025-12-31.
- **Decision**: Treat 2023-2025 as the immutable historical baseline; future refresh cycles R1 and R2 will project into 2026.
- **Consequences**: Codified in dbt models and verified in Stage 1 test suite.
- **Confidence**: HIGH
