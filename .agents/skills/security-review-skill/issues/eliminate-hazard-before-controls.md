---
categories: [security-practices]
domains: [backend]
---

# Eliminate Hazard First

**MUST** remove the hazardous capability first, then reduce exposure by design, and only then add protective controls.

**Why:** A control wrapping a dangerous feature is a promise to configure it correctly forever. Deleting the feature removes the failure class instead of managing it.

**Detect:** For each high-risk finding, check the chosen fix against the alternatives in order: remove, redesign, then control.

**References:** NIST SP 800-160v1r1, https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-160v1r1.pdf
