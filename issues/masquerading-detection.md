---
categories: [observability]
domains: [reliability]
---

# Masquerading & Homoglyph Detection

**SHOULD** detect lookalike process, service, and domain names built from homoglyphs or misspellings of trusted names (e.g. `crond` vs `cron`, `paypa1`).

**Why:** Attackers routinely disguise malware as legitimate binaries; name-similarity checks catch spoofing that hash allowlists miss entirely.

**Detect:** grep EDR/SIEM rules for homoglyph normalization, Levenshtein distance checks against known-good process lists, and lookalike domain monitoring.

**References:** MITRE ATT&CK T1036 Masquerading, T1036.008, CWE-456, Unicode homoglyphs (Trojan Source)
