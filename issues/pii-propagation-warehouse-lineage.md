# PII Propagation & Warehouse Lineage

**SHOULD** track where PII flows through warehouse layers (raw→staging→marts→exports) with lineage, and enforce classification at each hop.

**Why:** PII copied into analytics tables, temp datasets, and BI exports silently multiplies copies beyond the retention and access controls that protect the source.

**Detect:** review lineage tooling (OpenLineage, dbt lineage, DataHub/Collibra) for PII-tagged datasets; sample staging/mart tables for unclassified columns containing emails/ids; check export destinations inherit classification.

**References:** OpenLineage spec, GDPR Art. 5(1)(c) data minimisation, Snowflake/BigQuery data-classification docs
