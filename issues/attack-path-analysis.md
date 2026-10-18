# Attack-Path Analysis (reachable chains from exposure to crown jewels)

**SHOULD** continuously map reachable attack paths from internet exposure and low-privilege identities to critical assets, and cut the shortest chains first.

**Why:** Individual findings look minor in isolation; it's the composed chain — public bucket to role trust to database — that actually breaches you.

**Detect:** grep for attack-path tooling: `cartography`, `bloodhound`, `peanut`, Wiz/Knossos attack paths, `reachability` graph exports, `attack_path` reports in vuln management.

**References:** MITRE ATT&CK, NIST SP 800-30 (risk assessment), BloodHound docs, CSEM attack-path analysis
