---
categories: [mobile]
domains: [mobile]
---

# Header Controls Miss Non-Browsers

**MUST** enforce security controls for non-browser clients in client or server logic, never by relying on response headers those clients ignore.

**Why:** Mobile, SDK, and embedded HTTP clients do not implement HSTS, CSP, or frame protections, so a header-only defense does nothing for the traffic that carries tokens.

**Detect:** judgment — inspect the mobile or SDK HTTP layer for certificate validation, redirect refusal, and cookie handling implemented in code rather than assumed from server headers.

**References:** Security header support in HTTP clients, https://arxiv.org/abs/2111.03601
