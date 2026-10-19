---
categories: [web-client-security]
domains: [backend, frontend]
---

# SVG Active Content

**MUST** strip scripts, event handlers, and `foreignObject` from user-supplied SVG, or serve it as an image rather than inline markup.

**Why:** SVG is an HTML document with an XML syntax; an upload endpoint that renders it inline is a stored-XSS endpoint with an image extension.

**Detect:** grep for `image/svg`, `<svg` injected into templates, and for `.svg` accepted by upload allow-lists with no `foreignObject`/`onload` filtering.

**References:** OWASP ASVS v5.0 V1 Encoding and Sanitization, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x10-V1-Encoding-and-Sanitization.md
