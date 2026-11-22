# Documentation Risk Review: Workbook Business.Req.XRay

## 1. Audit of Claims, Case Studies & Statistics
| Item / Claim | Location | Category | Finding & Recommendation |
|---|---|---|---|
| McKesson 34% excursion reduction | C7 | UNSOURCED | Specific percentage not verified against primary public SEC filing. Reword to focus on verified enterprise architecture. |
| AmerisourceBergen $16.5M savings | C7 | UNSOURCED | Rephrase as illustrative case study benchmark. |
| AstraZeneca 45% stockout cut | C7 | UNSOURCED | Rephrase as standard industry cold-chain capability. |
| OTIF % Metric | C10 | OUT OF SCOPE | OTIF belongs to Phase 3 / Inbound logistics (Dataset 03). Mark as 'Phase 3 Scope'. |
| 'Make my C-suite happy for bonus' | OLTP.XRay C2 | UNPROFESSIONAL | Replace with formal business justification: 'Deliver 360-degree inventory intelligence'. |

## 2. Diagram Alignment Check
- Diagram correctly models Fact Constellation (`Fact_PharmacySales`, `Fact_Demand`, `Fact_Inventory`).
- In Stage 2, regenerate high-res PNG embedding role-playing date relationships clearly.
