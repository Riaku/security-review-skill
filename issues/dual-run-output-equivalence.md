# Dual-Run Output Equivalence

**SHOULD** run old and new processing paths in parallel and diff their outputs before cutting over for high-risk data/logic changes (the data-layer analogue of blue-green deployment).

**Why:** A rewritten pipeline or refactored calculation can be subtly wrong on data you didn't think to test; parallel-run diffing catches divergence on real inputs before users do.

**Detect:** check migration plans/runbooks for parallel-run + output-diff steps with tolerance thresholds; flag cutovers planned without equivalence verification.

**References:** blue-green/canary practice applied to data pipelines, migration dual-run guidance

---

**Part of:** [data-pipelines](../categories/data-pipelines.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
