---
categories: [correctness-pitfalls]
domains: [backend]
---

# Structured Exception Handling (typed errors, no swallowed exceptions, error boundaries)

**MUST** raise typed errors and catch them narrowly at defined boundaries; never blanket-catch and continue as if nothing failed.

**Why:** Untyped, swallowed exceptions erase the failure signal, so callers proceed on corrupt state and bugs become undiagnosable.

**Detect:** Bare `except:`/`catch(Exception)`, error logged but flow continues, no custom error classes, missing React error boundary at UI roots.

**References:** CWE-390, CWE-703, OWASP ASVS 7.4

---

**Part of:** [correctness-pitfalls](../categories/correctness-pitfalls.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
