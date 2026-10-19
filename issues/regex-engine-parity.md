---
categories: [web-api-security]
domains: [backend]
---

# Regex Engine Parity

**MUST** verify each validation pattern's behavior on the engine that runs it in production, not on the dialect it was copied from.

**Why:** Engines differ on anchoring, Unicode classes, backreferences and backtracking limits, so a copied validator can accept inputs its author tested as rejected.

**Detect:** Run the pattern corpus under the production engine (RE2, V8, JVM) and diff the results against the dialect the pattern was written for.

**References:** OpenSSF: Correctly Using Regular Expressions, https://best.openssf.org/Correctly-Using-Regular-Expressions, CWE-625
