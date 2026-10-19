---
categories: [compliance-privacy]
domains: [data]
---

# Minimize Personal Data Collected

**MUST NOT** add a personal-data field without a stated purpose, a retention period, and the code path that deletes it.

**Why:** You cannot leak what you never stored, and every extra field widens breach cost and the scope of every erasure request.

**Detect:** grep new PII columns in migrations (`email`, `phone`, `dob`, `address`, `ssn`, `ip`) with no matching retention or purge job and no erasure path.

**References:** OWASP User Privacy Protection Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/User_Privacy_Protection_Cheat_Sheet.html, GDPR Art. 25, https://eur-lex.europa.eu/eli/reg/2016/679/oj
