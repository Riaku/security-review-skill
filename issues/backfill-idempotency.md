---
categories: [data-pipelines]
domains: [data]
---

# Backfill Idempotency at Pipeline Scale

**MUST** make pipeline backfills/re-runs idempotent: reprocessing a date range produces the same result, never duplicates or double-counts.

**Why:** Every data team eventually re-runs a week of jobs; non-idempotent backfills double revenue figures or duplicate records that take months to discover and unwind.

**Detect:** check jobs use MERGE/upsert/overwrite-partition semantics vs append; look for run-id dedupe keys; review backfill runbook for "safe to re-run" statement per job.

**References:** DDIA idempotent consumers, dbt incremental materializations, Airflow clear/backfill semantics
