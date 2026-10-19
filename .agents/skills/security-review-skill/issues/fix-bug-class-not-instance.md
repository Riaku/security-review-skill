---
categories: [security-practices]
domains: [governance]
---

# Fix the Bug Class

**SHOULD** close a fixed vulnerability as a class, adding a mechanical check that fails on the same pattern elsewhere.

**Why:** The same weakness usually recurs in sibling handlers; fixing only the reported instance leaves the rest exploitable and unreported.

**Detect:** judgment: the fix commit — whether it adds a lint/semgrep rule or shared helper, or only patches one call site.

**References:** CWE Top 25 (2024), https://cwe.mitre.org/top25/archive/2024/2024_cwe_top25.html, NIST SP 800-218 SSDF, https://csrc.nist.gov/pubs/sp/800/218/final
