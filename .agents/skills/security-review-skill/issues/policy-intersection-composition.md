---
categories: [web-client-security]
domains: [frontend]
---

# Policy Intersection Composition

**MUST** compose overlapping policy layers by intersection, so the effective policy allows only what every layer allows.

**Why:** Ad-hoc layering produces union-shaped surprises where the looser layer wins silently and reviewers believe the strictest layer applied.

**Detect:** grep policy composition for `extend(`, `append(`, `add(` or `+` applied to source or allow lists where an intersection is intended.

**References:** W3C CSP Level 3, https://w3c.github.io/webappsec-csp/
