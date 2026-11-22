# ADR-013: Hospital Demand Fulfillment and Shortage Metric Definition

- **Status**: ACCEPTED
- **Date**: 2026-11-22
- **Context**: UnfulfilledDemandPacks strictly matches RequestedQuantityPacks - ConsumedQuantityPacks in 100% of demand records.
- **Decision**: Define hospital unfulfilled demand as Requested - Consumed; define service fill rate as Consumed / Requested.
- **Consequences**: Codified in dbt models and verified in Stage 1 test suite.
- **Confidence**: HIGH
