# SLAs

**SHOULD NOT** contract externally committed availability that internal SLOs and capacity cannot demonstrably sustain.

**Why:** An SLA looser than engineering reality triggers credits, churn, and legal exposure every time the system behaves as built.

**Detect:** SLA text vs `slo:` config mismatch, no credit policy, uptime claims without measurement source.

**References:** Google SRE Book (SLA/SLO/SLI), ISO 20000, NIST SP 800-144
