---
categories: [web-client-security]
domains: [backend, frontend]
---

# Encode at the Sink

**MUST** encode untrusted data for the consuming interpreter at the last step before it is interpreted, never when it is stored.

**Why:** A value encoded early is decoded or re-interpreted by the layers in between, so the protection is gone exactly where it was needed.

**Detect:** grep for escaping applied on write (`html.EscapeString`, `escapeHtml`, `htmlspecialchars`) in model setters or INSERT paths instead of in the view/template layer.

**References:** OWASP ASVS v5.0 V1 Encoding and Sanitization, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x10-V1-Encoding-and-Sanitization.md
