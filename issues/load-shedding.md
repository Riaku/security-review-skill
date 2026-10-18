# Load Shedding

**SHOULD** drop low-priority traffic under saturation so core transactions keep latency and availability targets.

**Why:** Undifferentiated processing lets bulk or abusive requests starve revenue-critical paths, so the worst case hurts everyone equally.

**Detect:** grep `shed`, `admission_control`, `priority_queue`, feature-flag gating of non-critical endpoints.

**References:** AWS Architecture Center load shedding, Google SRE Book SLO shedding, CWE-400, REL11-BP05
