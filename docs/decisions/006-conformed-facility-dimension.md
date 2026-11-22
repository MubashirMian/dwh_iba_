# ADR-006: Conformed DimFacility Hierarchy

- **Status**: ACCEPTED
- **Date**: 2026-11-22
- **Context**: Pharmacies (PHR001-050) and Hospitals (HOSP001-012) share zero overlapping IDs and identical geographical attributes.
- **Decision**: Union pharmacies and hospitals into a single conformed DimFacility dimension with FacilityType attribute.
- **Consequences**: Codified in dbt models and verified in Stage 1 test suite.
- **Confidence**: HIGH
