# DNSSEC

**SHOULD** Authoritative zones sign their records with DNSSEC, security-sensitive lookups use validating resolvers, and key rollover be automated and monitored.

**Why:** Unsigned DNS answers are forgeable by an on-path attacker or a compromised upstream resolver, silently redirecting users and services; DNSSEC makes forged answers cryptographically detectable.

**Detect:** Run `dig +dnssec <zone>` and check for `RRSIG` and the `AD` flag; verify the DS record exists in the parent. Watch for unmanaged KSK/ZSK rollover calendars — expired signatures break resolution as surely as an attack.

**Bad:**
```
$ dig example.com +dnssec     # no RRSIG, AD flag absent — unsigned zone
```

**Good:**
```
$ dig example.com +dnssec     # RRSIG present, AD set, DS in parent
# KSK rollover automated via registrar API with expiry alerts
```

**References:** RFC 4033/4034, RFC 6781 (key rollover), Cloudflare DNSSEC docs

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
