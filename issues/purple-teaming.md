---
categories: [security-practices]
domains: [backend]
---

# Purple Teaming (red+blue collaborative feedback loops)

**SHOULD** run structured purple-team sessions where red-team techniques are replayed against blue detections, closing each gap in both directions.

**Why:** Siloed red and blue teams optimize for scoring, not detection coverage; joint loops convert attacks into durable telemetry.

**Detect:** `purple-team` session reports, shared `detection-gap` backlog, ATT&CK coverage matrices with blue annotations

**References:** MITRE ATT&CK Evaluations, NIST SP 800-115, CISA Purple Team guidance

---

**Part of:** [security-practices](../categories/security-practices.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
