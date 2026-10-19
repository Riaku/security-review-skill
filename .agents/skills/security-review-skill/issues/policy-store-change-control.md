---
categories: [authorization-access-control]
domains: [governance]
---

# Policy Store Change Control

**MUST** restrict writes to the authorization policy store to dedicated administrators and log every policy change for review.

**Why:** Whoever can edit the policy decides every access decision, so an unreviewed policy edit is a silent grant of everything the policy covers.

**Detect:** kubectl auth can-i update on the policy custom resource for each subject; audit-log query for writes to policy objects.

**References:** NIST SP 800-207 §5.1, https://doi.org/10.6028/NIST.SP.800-207, NIST SP 800-53 AU-9
