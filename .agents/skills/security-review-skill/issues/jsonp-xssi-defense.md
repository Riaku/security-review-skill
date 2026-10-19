---
categories: [web-client-security]
domains: [backend]
---

# JSONP and XSSI Defense

**MUST NOT** expose authorized data through script-inclusion formats, or return JSON that another origin can read through a script tag.

**Why:** A callback-wrapped or bare JSON response is readable by any page that includes it, so authenticated data leaks without an XSS bug.

**Detect:** grep for `callback=`, `jsonp`, `jsoncallback` handlers and for JSON endpoints missing an anti-XSSI prefix or `Content-Type` enforcement.

**References:** OWASP ASVS v5.0, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x12-V3-Web-Frontend-Security.md, CWE-200
