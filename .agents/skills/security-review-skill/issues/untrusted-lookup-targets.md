---
categories: [supply-chain, web-api-security]
domains: [backend]
---

# Untrusted Lookup Targets

**MUST NOT** let untrusted input choose a name-resolution, class-loading, or remote-fetch target inside an interpreter or template.

**Why:** Lookup mechanisms turn a data field into code or network reach: a logged string becomes an outbound directory request, a filename becomes a loaded class. The attacker chooses what executes or where the request goes.

**Detect:** grep `InitialContext.lookup`, `Class.forName(`, `importlib.import_module`, dynamic `require(`/`import(` with request-derived arguments, and template calls that accept a variable template name.

**References:** Cloudflare Log4j response, https://blog.cloudflare.com/how-cloudflare-security-responded-to-log4j2-vulnerability/, OWASP Injection Prevention Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html, CWE-470 Use of Externally-Controlled Input to Select Classes or Code
