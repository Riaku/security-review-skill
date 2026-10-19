---
categories: [web-api-security]
domains: [backend]
---

# Signup Abuse Limits

**SHOULD** bound the resources a self-service account can consume — compute, storage, outbound sends, and spend — before payment or verification.

**Why:** Free tiers are farmed for cryptomining, file hosting, and outbound mail, and the operator pays. Per-account ceilings make bulk abuse unprofitable without blocking legitimate signups.

**Detect:** grep signup and quota code for per-account limits on jobs, storage, egress, and email sends; flag flows where verification happens only after resources are consumed.

**References:** OWASP Abuse Case Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Abuse_Case_Cheat_Sheet.html
