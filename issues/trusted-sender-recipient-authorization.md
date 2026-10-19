---
categories: [email-security]
domains: [backend]
---

# Trusted Sender Recipient Authorization

**MUST** authorize the recipient, template, and content of every user-triggered notification the service sends under its own trusted identity.

**Why:** When the actor choosing message parameters differs from the principal that signs and delivers, the service becomes an open relay that lends its domain reputation to whoever can drive it.

**Detect:** grep notification handlers that take `to`/`recipient` from the request body and call the mail or push provider without a recipient allowlist or template allowlist.

**References:** Trusted workflow relay analysis, https://arxiv.org/abs/2608.17361, CWE-441 (Confused Deputy)
