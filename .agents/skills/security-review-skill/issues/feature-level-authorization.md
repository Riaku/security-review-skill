---
categories: [authorization-access-control]
domains: [backend]
---

# Feature-Level Authorization

**MUST** check authorization against a named permission for the specific action, never a bare role string such as `role == "admin"`.

**Why:** `is_admin`-style checks re-hardcode the permission map into code, so every new feature silently inherits whatever the role string allows.

**Detect:** grep for role-string comparisons in handlers (`role == "admin"`, `isAdmin`, `user.role in (`) guarding feature or record-level operations.

**References:** OWASP ASVS v5.0 V8.2.1, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x17-V8-Authorization.md
