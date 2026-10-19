---
categories: [security-practices]
domains: [backend]
---

# Security Properties Decomposition

**MUST** analyze and document confidentiality, integrity and peer authentication as separate properties rather than one undifferentiated security goal.

**Why:** A single 'is it secure' goal cannot be tested or attributed to a mechanism. Named properties each get their own threat, mechanism and failure mode.

**Detect:** Inspect the design doc: each property has a stated mechanism and a stated failure condition.

**References:** RFC 3552, https://www.rfc-editor.org/rfc/rfc3552.txt
