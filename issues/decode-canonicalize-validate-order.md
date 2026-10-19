---
categories: [web-api-security]
domains: [backend]
---

# Decode Before Validate

**MUST** decode input fully, then canonicalize, then validate, so no later step can reinterpret data an earlier check already approved.

**Why:** Validating before decoding lets an encoded payload pass the check and then decode into a dangerous form downstream. Sanitizing instead of rejecting leaves the same gap.

**Detect:** Trace one tainted parameter from ingress to sink: record where decoding, canonicalization and validation happen and confirm that order.

**References:** SAFECode Fundamental Practices v3 (2018), https://safecode.org/wp-content/uploads/2018/03/SAFECode_Fundamental_Practices_for_Secure_Software_Development_March_2018.pdf, CWE-180
