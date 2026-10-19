---
categories: [security-practices]
domains: [backend]
---

# Vetted Implementations Over Bespoke Code

**SHOULD** implement authentication, authorization, parsing, and encoding with maintained, widely reviewed libraries rather than bespoke code.

**Why:** Shared implementations meet their failure modes earlier and are fixed once for everyone; a bespoke variant ships its first bug to production.

**Detect:** grep for hand-rolled crypto, base64, JWT, or auth helpers defined in-repo instead of a maintained library

**References:** OWASP Go Secure Coding Practices, https://github.com/OWASP/Go-SCP
