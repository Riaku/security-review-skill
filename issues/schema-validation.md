# Schema Validation

**MUST** validate every inbound payload against an explicit schema (types, required fields, bounds) before any business logic runs.

**Why:** Unvalidated fields let attackers inject unexpected shapes, extra keys, or oversized values that downstream code mishandles.

**Detect:** Handler reads `request.json[...]` with no validator, missing Pydantic/Zod/JSON Schema, `additionalProperties: true`, mass-assignment from raw body.

**References:** CWE-915, CWE-1289, OWASP ASVS 5.2, OWASP API1:2023

---

**Part of:** [correctness-pitfalls](../categories/correctness-pitfalls.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
