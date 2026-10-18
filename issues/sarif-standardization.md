---
categories: [cicd-pipeline-security, observability]
domains: [infrastructure, reliability]
---

# SARIF-Standardized Scan Results (unified alert pipeline)

**SHOULD** emit all scanner findings in SARIF and ingest them into one dashboard, because scattered formats hide coverage gaps and duplicate triage.

**Why:** Findings in per-tool logs go unseen; a unified pipeline makes severity trends and deduplication auditable.

**Detect:** Scanners run without `--format sarif` / `output: sarif`; no upload step to code-scanning API; each tool reporting to a separate ad-hoc log file.

**References:** CWE-1053, NIST SP 800-218 (SSDF), SARIF spec (OASIS), GitHub code scanning SARIF upload docs
