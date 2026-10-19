---
categories: [authorization-access-control]
domains: [backend]
---

# Independent Conditions for Irreversible Actions

**MUST** require irreversible high-consequence actions to satisfy independent authorization, environment, and intent conditions drawn from different trust domains before executing.

**Why:** A single compromised credential or channel then cannot trigger the action alone, however privileged that compromise is.

**Detect:** judgment: the authorization flow for the destructive action — count the independent conditions and their sources

**References:** Anderson, Security Engineering 3rd ed., ch.15, https://www.cl.cam.ac.uk/~rja14/Papers/SEv3-ch15.pdf
