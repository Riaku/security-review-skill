---
categories: [compliance-privacy]
domains: [data]
---

# Quasi-Identifier Class Floors

**MUST** measure quasi-identifier combinations in any released dataset and suppress or generalise rows until every equivalence class meets a minimum size, instead of only stripping direct identifiers.

**Why:** Date of birth, postcode and sex together single out most people, so a release with names removed still re-identifies from public records while being labelled de-identified.

**Detect:** command: run `arx`, `sdcMicro`, or a groupby over candidate quasi-identifier columns and report the smallest equivalence-class size; flag any release whose floor is below policy (commonly 5–11).

**References:** NIST SP 800-188 De-Identifying Government Datasets, https://csrc.nist.gov/pubs/sp/800/188/final, Sweeney, k-anonymity (1997), ENISA pseudonymisation techniques, https://www.enisa.europa.eu/publications/pseudonymisation-techniques-and-best-practices
