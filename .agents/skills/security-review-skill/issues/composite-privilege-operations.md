---
categories: [authorization-access-control]
domains: [backend]
---

# Composite Privilege from Innocuous Operations

**MUST** review and audit the low-privilege operations around a protected asset in combination, because individually harmless edits compose into privilege the operator does not otherwise hold.

**Why:** Address change, card issue, and address revert are each harmless alone and amount to account takeover in sequence, and audits covering only sensitive-sounding operations miss it.

**Detect:** judgment: the admin operation inventory, enumerated as sequences that reach a sensitive outcome

**References:** Anderson, Security Engineering 3rd ed., ch.12, https://www.cl.cam.ac.uk/~rja14/Papers/SEv3-ch12.pdf
