# SOC 2

**SHOULD** implement controls mapped to Trust Services Criteria (security, availability, confidentiality) with evidence collection automated.

**Why:** Gaps in control coverage cause audit failures, lost enterprise deals, and inability to demonstrate security posture to customers.

**Detect:** grep for missing control mappings in compliance-as-code; check `trust_service_criteria`, `control_id`, evidence automation config absent.

**References:** AICPA TSC CC1-CC9, SOC 2 Type II, ISO 27001 Annex A
