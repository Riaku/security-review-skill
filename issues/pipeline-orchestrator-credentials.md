# Pipeline-Orchestrator Credential Sprawl

**MUST** centralize credentials used by data orchestrators (Airflow connections, dbt profiles, Spark configs) in a secrets backend — not in DAG files, connections tables in plaintext, or CI env dumps.

**Why:** Orchestrators hold keys to every warehouse, bucket, and DB in the estate; their configs are broadly readable by data teams, making them the flattest credential attack surface in the company.

**Detect:** grep DAGs/profiles for inline passwords, check Airflow Connections backend (secrets env/backend vs metadata DB plaintext), review dbt `profiles.yml` handling, inspect Spark `--conf` for hardcoded AWS keys.

**References:** Airflow secrets-backend docs, dbt secure credentials guidance, OWASP Data Security

---

**Part of:** [data-pipelines](../categories/data-pipelines.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
