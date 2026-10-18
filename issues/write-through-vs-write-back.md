---
categories: [caching]
domains: [reliability]
---

# Write-Through vs Write-Back

**MUST** use write-through persistence for security-relevant records (audit logs, ACLs, tokens); write-back caching is prohibited where a crash must not lose the write.

**Why:** Write-back buffers durable security events in volatile memory, so a crash silently drops audit trails and authorization changes.

**Detect:** Redis `appendonly no`, async flush settings, or deferred DB writes on audit/ACL tables; `write_back`, `async_write` flags.

**References:** OWASP A09:2021, CWE-758, NIST SP 800-53 AU-9, AU-4

---

**Part of:** [caching](../categories/caching.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
