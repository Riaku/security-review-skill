# data-pipelines — full checklist (3 items)

ETL/orchestration security: pipeline creds, lineage, backfill safety.

> Generated artifact. Canonical source: `issues/<slug>.md`.

# Pipeline-Orchestrator Credential Sprawl

**MUST** centralize credentials used by data orchestrators (Airflow connections, dbt profiles, Spark configs) in a secrets backend — not in DAG files, connections tables in plaintext, or CI env dumps.

**Why:** Orchestrators hold keys to every warehouse, bucket, and DB in the estate; their configs are broadly readable by data teams, making them the flattest credential attack surface in the company.

**Detect:** grep DAGs/profiles for inline passwords, check Airflow Connections backend (secrets env/backend vs metadata DB plaintext), review dbt `profiles.yml` handling, inspect Spark `--conf` for hardcoded AWS keys.

**References:** Airflow secrets-backend docs, dbt secure credentials guidance, OWASP Data Security

# PII Propagation & Warehouse Lineage

**SHOULD** track where PII flows through warehouse layers (raw→staging→marts→exports) with lineage, and enforce classification at each hop.

**Why:** PII copied into analytics tables, temp datasets, and BI exports silently multiplies copies beyond the retention and access controls that protect the source.

**Detect:** review lineage tooling (OpenLineage, dbt lineage, DataHub/Collibra) for PII-tagged datasets; sample staging/mart tables for unclassified columns containing emails/ids; check export destinations inherit classification.

**References:** OpenLineage spec, GDPR Art. 5(1)(c) data minimisation, Snowflake/BigQuery data-classification docs

# Backfill Idempotency at Pipeline Scale

**MUST** make pipeline backfills/re-runs idempotent: reprocessing a date range produces the same result, never duplicates or double-counts.

**Why:** Every data team eventually re-runs a week of jobs; non-idempotent backfills double revenue figures or duplicate records that take months to discover and unwind.

**Detect:** check jobs use MERGE/upsert/overwrite-partition semantics vs append; look for run-id dedupe keys; review backfill runbook for "safe to re-run" statement per job.

**References:** DDIA idempotent consumers, dbt incremental materializations, Airflow clear/backfill semantics

