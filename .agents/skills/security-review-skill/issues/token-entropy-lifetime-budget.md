---
categories: [authentication]
domains: [backend]
---

# Token Entropy and Lifetime

**MUST** size token entropy and lifetime together, so a token under 128 bits of entropy is rate-limited and expires within minutes.

**Why:** Entropy and validity multiply into brute-force feasibility; a slightly weak identifier that expires in minutes is a different risk from one valid for a week.

**Detect:** grep token generation and its TTL side by side (`secrets.token_hex(8)`, `uuid1`, `random`) against `expires_in`, `max_age`, and session timeout config.

**References:** OWASP WSTG Session Management Schema, https://github.com/OWASP/wstg/blob/master/document/4-Web_Application_Security_Testing/06-Session_Management/01-Session_Management_Schema.md
