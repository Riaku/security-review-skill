---
categories: [web-client-security]
domains: [backend, frontend]
---

# Maintained HTML Sanitizer

**MUST** sanitize untrusted rich-text HTML with a maintained allow-list sanitizer library, never a hand-written filter.

**Why:** Mutation-XSS bypasses any regex or tag-stripping filter you write; sanitizer maintainers absorb a parser-differential treadmill you cannot.

**Detect:** grep for bespoke sanitizers (`re.sub` on `<script`, `strip_tags`, custom `sanitize_html` helpers) and confirm an allow-list library (DOMPurify, bleach, sanitize-html, OWASP Java HTML Sanitizer) is the only path.

**References:** OWASP ASVS v5.0 V1 Encoding and Sanitization, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x10-V1-Encoding-and-Sanitization.md
