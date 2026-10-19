---
categories: [authorization-access-control]
domains: [backend]
---

# Pending Dual-Approval State

**MUST** persist partially approved transactions in a store protected like the action itself, with expiry, cancellation rules, and visibility limited to the approvers.

**Why:** Dual control is not atomic: between the two sign-offs the half-approved request is state an attacker can replay, cancel, or complete.

**Detect:** judgment: the approval workflow's pending table and who may read, cancel, or extend its entries

**References:** Anderson, Security Engineering 3rd ed., ch.12, https://www.cl.cam.ac.uk/~rja14/Papers/SEv3-ch12.pdf
