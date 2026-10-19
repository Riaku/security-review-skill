---
categories: [authentication]
domains: [backend]
---

# Session Lifetime Limits

**MUST** enforce both an idle timeout and an absolute maximum session lifetime, requiring re-authentication when either is exceeded.

**Why:** An idle timeout alone lets a continuously refreshed session live forever, while an absolute cap alone leaves an unattended terminal authenticated. A stolen cookie only needs to be kept warm.

**Detect:** grep session and cookie configuration for `maxAge`, `idleTimeout`, `expires`, and refresh-token lifetime; flag sessions with no absolute cap or refresh that extends past it.

**References:** OWASP Session Management Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html, NIST SP 800-63B reauthentication requirements
