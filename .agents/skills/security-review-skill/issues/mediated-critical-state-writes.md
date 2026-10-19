---
categories: [database]
domains: [data]
---

# Mediated Writes to Critical State

**MUST** route every write to critical state through a constrained set of procedures that enforce a declared invariant, and verify that invariant independently of the writer.

**Why:** Any path that writes the store directly — an admin console, a script, an ORM call — bypasses the checks the application layer believes are universal.

**Detect:** grep for UPDATE/INSERT/db.execute calls outside the service layer, and for every credential able to write the table directly

**References:** Anderson, Security Engineering 3rd ed., ch.12, https://www.cl.cam.ac.uk/~rja14/Papers/SEv3-ch12.pdf
