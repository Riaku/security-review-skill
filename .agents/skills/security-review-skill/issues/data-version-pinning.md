---
categories: [data-pipelines]
domains: [data]
---

# Data Version Pinning

**SHOULD** pin the exact version of input datasets used to produce any output (DVC, immutable versioned files, recorded dataset hashes) so results are re-derivable and auditable.

**Why:** Code provenance without data provenance can't answer "what evidence was this decision based on" — the same code on drifted data silently produces different answers.

**Detect:** check for data-versioning tooling (DVC lock files, dataset manifests with hashes) or recorded input versions in output metadata; flag pipelines reading mutable "latest" datasets without pinning.

**References:** DVC docs, data lineage/provenance practice, reproducible-research data management guidance
