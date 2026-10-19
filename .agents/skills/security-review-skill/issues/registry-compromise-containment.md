---
categories: [sre-incidents, supply-chain]
domains: [infrastructure]
---

# Registry Compromise Containment

**MUST** maintain a rehearsed procedure to mass-revoke registry and CI tokens and block compromised package versions within hours.

**Why:** Automated worms publish across thousands of packages and consume every token they can reach in minutes. Manual, per-incident rotation cannot keep pace with registry-scale compromise.

**Detect:** judgment: the incident runbook and its last exercise record — token inventory, bulk-revocation path, and a dependency freeze/blocklist mechanism with a measured time-to-contain.

**References:** GitHub: disrupting supply-chain attacks on npm and GitHub Actions, https://github.blog/security/supply-chain-security/disrupting-supply-chain-attacks-on-npm-and-github-actions/
