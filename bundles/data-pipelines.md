# data-pipelines — full checklist (7 items)

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

# Interactive-Session Artifact Leakage

**MUST NOT** commit interactive-session artifacts (notebooks with executed outputs, REPL dumps, workspace snapshots) that embed the actual data processed during the session.

**Why:** Executed notebooks persist every row/chart they touched inside the committed file — sensitive data ships silently with code review, forks, and clones, invisible to diff tools that show only code.

**Detect:** grep tracked notebook/JSON files for embedded result payloads (`"outputs"`, base64 blobs, table rows); check for output-stripping pre-commit hooks or CI checks on committed notebooks.

**References:** analysis-code reproducibility guidance, nbstripout/ClearOutputPreprocessor tooling

# Data Version Pinning

**SHOULD** pin the exact version of input datasets used to produce any output (DVC, immutable versioned files, recorded dataset hashes) so results are re-derivable and auditable.

**Why:** Code provenance without data provenance can't answer "what evidence was this decision based on" — the same code on drifted data silently produces different answers.

**Detect:** check for data-versioning tooling (DVC lock files, dataset manifests with hashes) or recorded input versions in output metadata; flag pipelines reading mutable "latest" datasets without pinning.

**References:** DVC docs, data lineage/provenance practice, reproducible-research data management guidance

# Raw-Data Immutability

**MUST NOT** modify raw source data in place; transformations operate on copies, preserving the raw layer for re-derivation and audit.

**Why:** Edited raw data destroys the ability to re-audit cleaning decisions, re-run pipelines correctly, or prove what the original evidence said.

**Detect:** check storage layout for read-only raw layer (permissions, separate bucket/schema) vs in-place edits; review pipeline code for writes to raw datasets; check raw retention policy.

**References:** analysis data-management guidance (raw-as-read-only), medallion architecture raw-layer immutability

# Dual-Run Output Equivalence

**SHOULD** run old and new processing paths in parallel and diff their outputs before cutting over for high-risk data/logic changes (the data-layer analogue of blue-green deployment).

**Why:** A rewritten pipeline or refactored calculation can be subtly wrong on data you didn't think to test; parallel-run diffing catches divergence on real inputs before users do.

**Detect:** check migration plans/runbooks for parallel-run + output-diff steps with tolerance thresholds; flag cutovers planned without equivalence verification.

**References:** blue-green/canary practice applied to data pipelines, migration dual-run guidance

