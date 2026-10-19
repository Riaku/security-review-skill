---
categories: [web-api-security]
domains: [backend]
---

# Strict Parser Rejection

**MUST** reject malformed, ambiguous, or non-canonical input at security-critical parsers instead of tolerating it for interoperability.

**Why:** Tolerant receivers keep non-conformant implementations alive and turn undefined behaviour into a permanent compatibility constraint that cannot be patched.

**Detect:** grep parsers for lenient switches (`strict=False`, `allow_unknown`, duplicate-header tolerance, trailing-garbage acceptance) and for fallback branches that repair bad input.

**References:** NCSC Protocol Design Principles, https://www.ncsc.gov.uk/sites/default/files/2026-06/Protocol-Design-Principles.pdf
