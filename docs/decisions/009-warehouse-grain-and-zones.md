# ADR-009: Warehouse Dimension Grain and Storage Zones

- **Status**: ACCEPTED
- **Date**: 2026-11-22
- **Context**: Warehouse attributes (Name, GLN, Capacity) are functionally dependent on WarehouseID; zones vary within warehouses.
- **Decision**: Model DimWarehouse at Warehouse level and carry StorageZoneID as zone attribute.
- **Consequences**: Codified in dbt models and verified in Stage 1 test suite.
- **Confidence**: HIGH
