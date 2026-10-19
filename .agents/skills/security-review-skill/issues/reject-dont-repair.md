---
categories: [web-api-security]
domains: [backend]
---

# Reject, Don't Repair

**SHOULD** reject malformed input outright instead of sanitizing or correcting it toward validity and passing the repaired value on.

**Why:** A sanitizer encodes one component's idea of clean, and attackers live in the gap between what it strips and what the next consumer interprets.

**Detect:** grep `sanitize`, `strip_tags`, `escape`, `clean(`, `replace('<'` applied to request data before validation, and handlers that continue after a repair.

**References:** OWASP Input Validation Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
