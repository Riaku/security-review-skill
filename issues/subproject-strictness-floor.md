---
categories: [security-practices]
domains: [governance]
---

# Subproject Strictness Floor

**MUST** enforce security requirements in every subproject at least as strictly as the primary codebase.

**Why:** The weakest subproject sets the project's real posture, and auxiliary repositories typically skip the gates the main one enforces.

**Detect:** command compare required checks and scanner config across repos (`gh api repos/{owner}/{repo}/branches/main/protection`, CI config diff) and flag any subset.

**References:** OpenSSF OSPS Baseline: subproject security requirements, https://www.bestpractices.dev/en/criteria
