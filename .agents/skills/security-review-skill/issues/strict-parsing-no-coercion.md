---
categories: [web-api-security]
domains: [backend]
---

# Strict Parsing, No Coercion

**MUST** parse untrusted structured data with a strict schema that rejects unknown fields, duplicate keys, and type coercion.

**Why:** Lenient parsers silently coerce, and the coerced value differs from what the sender meant and from what the validator checked.

**Detect:** grep `additionalProperties: true`, `ignore_unknown_fields`, `strict=False`, `coerce`, `Extra`-allowing serializers, and schema-less `json.loads` on request bodies.

**References:** OWASP Input Validation Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
