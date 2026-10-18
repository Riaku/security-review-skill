# Attack-Path Analysis (reachable chains from exposure to crown jewels)

**SHOULD** continuously map reachable attack paths from internet exposure and low-privilege identities to critical assets, cutting shortest chains first.

**Why:** Findings look minor in isolation; it's the composed chain — public bucket to role trust to database — that actually breaches you.

**Detect:** grep for `cartography`, `bloodhound`, `attack_path` reports, reachability graph exports, CSEM attack-path tooling output.

**References:** MITRE ATT&CK, NIST SP 800-30 (risk assessment), BloodHound docs, CSEM attack-path analysis
