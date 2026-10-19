---
categories: [supply-chain]
domains: [infrastructure]
---

# Reachability-Aware Dependency Alerts

**SHOULD** alert only on vulnerable dependencies whose affected code path is reachable, and verify fixes against current versions.

**Why:** Volume-based update noise trains teams to ignore advisories, including the one that matters. Reachability turns a list of version bumps into a short list of real exposures.

**Detect:** `govulncheck ./...` or `osv-scanner --call-analysis=all` compared against a version-only scan.

**References:** Filippo Valsorda: dependabot, https://words.filippo.io/dispatches/dependabot/
