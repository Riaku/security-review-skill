# CAP Theorem

**SHOULD** document, per datastore, the explicit consistency-versus-availability tradeoff chosen under partition, and test it.

**Why:** Teams assume both guarantees; during a network partition the undeclared behavior surfaces as silent data loss or total outage.

**Detect:** grep config for `consistency=`, `read_preference=`, `quorum` vs `ONE`, `r/w` settings; missing partition-tolerance test in CI or runbook.

**References:** NIST SP 800-190, PACELC paper, AWS Well-Architected Reliability Pillar
