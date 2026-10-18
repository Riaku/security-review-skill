---
categories: [authentication]
domains: [backend]
---

# SAML assertion validation and XML signature wrapping

**MUST** validate the SAML assertion's signature against a pinned IdP certificate and verify the signed element is the one consumed, rejecting wrapping attacks.

**Why:** XML signature wrapping lets an attacker embed a validly-signed assertion inside a malicious one, tricking the SP into trusting attacker-controlled attributes.

**Detect:** grep SAML consumer for missing `signature` validation, no certificate pinning, parsing `Assertion` without checking `Signature` reference URI, `xmldsig` verification skipped.

**References:** CWE-347, OWASP A02:2021, CVE-2017-11427, SAML Security BCP §4.1.5
