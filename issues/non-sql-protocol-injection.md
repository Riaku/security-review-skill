---
categories: [web-api-security]
domains: [backend]
---

# Non-SQL Protocol Injection

**MUST** escape or reject untrusted values before they reach cache keys and mail command parsers.

**Why:** Every protocol has its own metacharacters; a value that is safe in SQL still injects LDAP filters, cache-key namespaces, or SMTP commands.

**Detect:** grep sinks: `memcache.get/set` and Redis key builders using concatenated request values, `sendmail(`, and `SMTP.send_message` built from request data.

**References:** OWASP ASVS v5.0 V1 Encoding and Sanitization, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x10-V1-Encoding-and-Sanitization.md
