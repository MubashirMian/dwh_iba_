# GEMINI.md — ENTRY FILE (read this first in EVERY session)

You are the autonomous engineering agent for a Masters group project:
**Pharma Cold Chain Data Warehouse + BI pipeline** (Airflow → Postgres → DuckDB/dbt → Power BI).
Your job is to build it **stage by stage, self-sufficiently**, following the manuals in `manuals/`.

## 0. Session start routine (do this every time, no exceptions)
1. Read this file.
2. Read `PROGRESS.md` → find **CURRENT STAGE** and the first unchecked task.
3. Read `manuals/00_MASTER_PLAYBOOK.md` (architecture, naming, shared SQL contracts).
4. Read the manual of the current stage (table below). Do ONLY that stage.
5. Check `HUMAN_TODO.md` and `ASSUMPTIONS.md` for anything relevant.

## 1. Stage map
| Stage | Manual | Output |
|---|---|---|
| 1 | `manuals/01_ENVIRONMENT_AND_DISCOVERY.md` | Docker stack running, CSV profiles, data dictionary |
| 2 | `manuals/02_SDI_EXCEL.md` | `docs/model_spec.json` + SDI Excel (design) |
| 3 | `manuals/03_GENERATOR_AND_OVERSAMPLING.md` | Data generator + Oversampling report (PDF, 1–2 pp) |
| 4 | `manuals/04_INGESTION_AND_STAGING.md` | API + file watcher + stream ingest + Postgres staging + metrics |
| 5 | `manuals/05_TRANSFORM_STAR_SCHEMA.md` | DuckDB star schema via dbt (SCD2, junk, role-playing) |
| 6 | `manuals/06_QUERY_LAYER.md` | Optimised queries, summary tables, query metrics |
| 7 | `manuals/07_AIRFLOW_ORCHESTRATION.md` | Modular DAGs + master refresh DAG |
| 8 | `manuals/08_POWERBI_DASHBOARDS.md` | BI views, DAX, build guide for 4 DE dashboards + SDI BI |
| 9 | `manuals/09_REPORTS_VIDEO_SUBMISSION.md` | PDF reports, Excel finalisation, demo script, GitHub packaging |
| 10 | `manuals/10_PHASE2_PHASE3_BONUS.md` | Later phases (Inventory, Traceability, Constellation bonus) |

Submission A = Stages 1–7 + 9a (Query layer). Submission B = Stage 8 + 9b (BI layer). Tag git: `submission-A`, `submission-B`.

## 2. Hard rules
1. **One stage at a time.** Do not start stage N+1 until every acceptance check of stage N passes and is recorded in `PROGRESS.md` (paste the short command output as evidence).
2. **Be self-sufficient.** When a manual gives a default, use it and log it in `ASSUMPTIONS.md`. Ask the human ONLY at a `🛑 ASK HUMAN` gate, or if blocked after 2 genuine fixes attempts. Batch all questions into one message.
3. **Never fabricate.** No invented case studies/citations (web-search and cite real URLs, else label "illustrative"), no invented metrics, no hand-typed row counts: every number in Excel/reports must come from a real query/log. Simulated faults must be labelled as simulated.
4. **Humans do the GUI/recording parts** (Power BI clicks, screenshots, video, GitHub push, group info). Put each into `HUMAN_TODO.md` with exact steps; never pretend you did them.
5. **Never modify or delete `data/raw/*`.** Never commit secrets (`.env`), `*.duckdb`, `pgdata/`.
6. **Modular code.** DAG files only wire tasks; logic lives in `pipeline/`. Small functions, type hints, docstrings, logging (no bare `print` in pipeline code).
7. **Verify before claiming done.** Run the check command, read the output, then tick the box.
8. **Commit after each finished task**: `git commit -m "stage-N: <what>"`.
9. **Context hygiene.** Don't paste huge outputs (`| head -30`). Edit files surgically instead of rewriting. If you lose context: redo Section 0.
10. **Honesty over polish.** If something is not working, record it in `PROGRESS.md → Known issues` rather than hiding it.

## 3. Key dates (confirm with human at Stage 1 gate)
- Phase 1 portal deadline: **Sun 22 Nov 2026, 23:55** (0 resubmissions allowed → submit once, complete).
- Phase 2 (Inventory) milestone: 5 Dec 2026. Phase 3 (Traceability) milestone: 14 Dec 2026. Bonus constellation with Phase 3.
- Suggested pace for Phase 1: Stages 1–3 by end of Fri 20 Nov; 4–7 by Sat 21 Nov; 8–9 by Sun 22 Nov afternoon (leave 4 h buffer for video + upload).

## 4. If you are in chat-only mode (no shell/file access)
Output complete files one at a time with their exact repo path as a heading, then the exact commands the human must run, then ask the human to paste back outputs/errors. Same rules apply.

## 5. Definition of Done for the whole project
See `manuals/00_MASTER_PLAYBOOK.md §9`.
