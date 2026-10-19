---
categories: [iot-embedded]
domains: [iot-embedded]
---

# Bounded Contributor Influence

**SHOULD** weight and cap each contributor's influence on an aggregated dataset so a small number of spoofed inputs cannot move the aggregate.

**Why:** Fusion amplifies: a handful of fabricated reports can register a system-wide condition, and every downstream decision inherits the fabrication.

**Detect:** judgment: the aggregation rule — per-source weight caps and outlier damping

**References:** Anderson, Security Engineering 3rd ed., ch.25, https://www.cl.cam.ac.uk/~rja14/Papers/SEv3-ch25.pdf
