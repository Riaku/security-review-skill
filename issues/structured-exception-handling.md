---
categories: [correctness-pitfalls]
domains: [backend]
---

# Structured Exception Handling (typed errors, no swallowed exceptions, error boundaries)

**MUST** raise typed errors and catch them narrowly at boundaries that can recover, propagating everything else with context instead of letting it vanish or continuing as if nothing failed.

**Why:** Untyped, swallowed exceptions erase the failure signal, so callers proceed on corrupt state, generic handlers leak stack traces to users, and bugs become undiagnosable.

**Detect:** Bare `except:`/`catch(Exception)`, `except Exception: pass`, `catch {}`, `catch (e) {}`, `.catch(() => {})`, ignored `err != nil`, error logged but flow continues, no custom error classes, missing React error boundary at UI roots.

**References:** CWE-390, CWE-209, CWE-703, OWASP ASVS 7.4
