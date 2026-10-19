---
categories: [security-practices]
domains: [governance, infrastructure]
---

# Legacy Asset Compensating Controls

**MUST** place compensating controls at the boundary of any asset that cannot adopt current authentication or cryptography, and record the accepted gap.

**Why:** Extended-lifecycle devices outlive the primitives around them, so exposure has to be absorbed by segmentation and monitoring rather than by the device.

**Detect:** Take the asset inventory's end-of-support entries and confirm each has a named boundary control and an owner.

**References:** NCSC Operational Technology collection, https://www.ncsc.gov.uk/collection/operational-technology
