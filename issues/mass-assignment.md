---
categories: [web-api-security]
domains: [backend]
---

# Mass Assignment

**MUST** Whitelist assignable fields when binding request bodies to models.

**Why:** Attackers add hidden fields like `is_admin` to escalate privileges or bypass rules.

**Detect:** `Model(**request.json)`, `save(params)`, `bindAll`; no allowed/forbidden lists in serializers.

**References:** OWASP A08:2021, CWE-915, Rails mass-assignment guide
