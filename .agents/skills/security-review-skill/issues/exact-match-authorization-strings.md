---
categories: [authorization-access-control]
domains: [backend]
---

# Exact-Match Authorization Strings

**MUST** compare roles, scopes, token claims, and paths by exact equality; never decide authorization with prefix, suffix, or substring matching.

**Why:** A startsWith("admin") check accepts administrator-disabled, and case folding silently widens the accepted set beyond the intended value.

**Detect:** grep startsWith(, endsWith(, includes(, HasPrefix, Contains( on role, claim, or path variables next to authorization code

**References:** Trail of Bits Testing Handbook, https://github.com/trailofbits/testing-handbook
