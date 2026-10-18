# SOC 2 as Audit Regime (CCs, evidence collection)

**SHOULD** collect continuous, timestamped evidence for Trust Services Criteria (security, availability, confidentiality) rather than assembling artifacts only at audit time.

**Why:** Point-in-time evidence gathering misses control gaps during the period; auditors sample exceptions the team never noticed.

**Detect:** grep for "TSC", "CC6", "CC7" mappings; missing access review logs, change tickets, monitoring alerts as evidence; manual-only evidence folders.

**References:** AICPA TSC 2017, SOC 2 Type II, Trust Services Criteria
