# data-pipelines

ETL/orchestration security: pipeline creds, lineage, backfill safety.

## What this category covers

This category covers the movement and transformation of data between stores: the ETL and orchestration layer that reads raw sources, produces derived datasets, and lands them for downstream consumers. Its member items span orchestrator credential handling, PII propagation and lineage across warehouse layers, backfill idempotency, raw-data immutability, dataset version pinning, dual-run equivalence for risky transformations, and leakage through interactive-session artifacts. A reviewer here should follow a single derived output back to its inputs and confirm the result is reproducible, the raw layer is untouched, and any personal data is classified at each hop. The recurring failure is a pipeline that cannot be re-run safely: a backfill that double-counts, raw data mutated in place, or a notebook committed with real data in its outputs.

- Orchestrator credential handling: Airflow connections, dbt profiles, Spark configs, CI env.
- Lineage and PII classification across raw, staging, mart, and export layers.
- Backfill and re-run idempotency at date-range scale.
- Raw-layer immutability and dataset version pinning for reproducibility.
- Interactive-session artifact hygiene and dual-run equivalence for risky changes.

## What it does not cover

- [database](../categories/database.md) — schema, queries, transactions, and backup of operational stores belong there; warehouse transforms and lineage belong here.
- [cicd-pipeline-security](../categories/cicd-pipeline-security.md) — the software build and deploy pipeline belongs there; data orchestration workflows belong here, despite the shared word "pipeline".
- [compliance-privacy](../categories/compliance-privacy.md) — retention policy, consent, and data-subject rights belong there; enforcing classification and propagating deletion through warehouse layers belongs here.
- [supply-chain](../categories/supply-chain.md) — artifact and build provenance belong there; pinning input datasets so derived results stay re-derivable belongs here.

## What a finding here looks like

- a backfill for a date range that re-emits rows already counted, inflating the total.
- an Airflow connection or dbt profile holding a plaintext production password in the repo.
- a notebook committed with executed cells that embed the real customer rows it processed.
- a transform writing back into the raw source table instead of operating on a copy.
- PII flowing from raw into an exported mart with no lineage record or classification.
