---
categories: [correctness-pitfalls, web-api-security]
domains: [backend]
---

# Input Validation

**MUST** validate every value entering the system at the trust boundary against an explicit server-side schema — types, required fields, lengths, ranges, and format allowlists — before any business logic runs.

**Why:** Downstream code assumes validated data; one unchecked field becomes the injection vector, and unvalidated fields let attackers inject unexpected shapes, extra keys, or oversized values that downstream code mishandles. A client-side check is UX only: the attacker disables JavaScript or posts to the API directly, so a form-level validator never runs on the request that matters.

**Detect:** Handlers reading `request.params`/body straight into logic; missing pydantic/Zod/Joi or `@Valid`; `request.json[...]` read with no validator or JSON Schema, `additionalProperties: true`, mass-assignment from raw body; a validator that exists only in frontend form code (a `zod`/`yup` schema imported by a React component) with no matching server-side schema on the route it posts to.

**References:** OWASP A03:2021, CWE-20, OWASP Input Validation Cheat Sheet, CWE-915, CWE-1289, OWASP ASVS V5.1.3/V5.1.4, OWASP API1:2023
