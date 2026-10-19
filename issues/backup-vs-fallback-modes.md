---
categories: [sre-incidents]
domains: [reliability]
---

# Backup Is Not Fallback

**MUST** design and rehearse backup restoration and degraded fallback operation as two separate modes with separate success criteria.

**Why:** Conflating them leaves the manual degraded mode unpracticed and the restore path assumed working, so the outage exercises the capability nobody tested.

**Detect:** judgment — inspect the runbook for distinct restore and fallback procedures, each with a last-tested date and its own acceptance check.

**References:** Anderson, Security Engineering 3e, ch.7 (backup vs fallback), https://www.cl.cam.ac.uk/~rja14/Papers/SEv3-ch07.pdf
