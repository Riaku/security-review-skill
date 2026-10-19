---
categories: [web-api-security]
domains: [backend]
---

# Regex Metacharacter Escaping

**MUST** escape or reject regex metacharacters in user input that becomes part of a pattern.

**Why:** Unescaped input lets the caller inject alternation and quantifiers, turning a search filter into a match-everything bypass or an exfiltration primitive.

**Detect:** grep `new RegExp(`, `re.compile(` and `Pattern.compile(` calls whose argument interpolates a request value rather than a literal.

**References:** OWASP ASVS v5.0 V1 Encoding and Sanitization, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x10-V1-Encoding-and-Sanitization.md
