# MTA-STS & TLS Reporting

**SHOULD** publish MTA-STS policy (or DANE) requiring TLS for inbound mail, with TLS-RPT monitoring for downgrade attempts.

**Why:** Without MTA-STS, mail can be downgraded to plaintext or redirected via MX hijack silently; TLS-RPT surfaces the interception attempts you'd otherwise never see.

**Detect:** `dig _mta-sts.<domain> TXT` and `https://mta-sts.<domain>/.well-known/mta-sts.txt` for policy (mode=enforce); check `_smtp._tls.<domain>` TLS-RPT record exists.

**References:** RFC 8461 MTA-STS, RFC 8472 TLS-RPT, Google Postmaster Tools

---

**Part of:** [email-security](../categories/email-security.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
