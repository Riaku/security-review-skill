---
categories: [api-design]
domains: [backend]
---

# HTTP/3 / QUIC

**SHOULD** validate that UDP 443 QUIC traffic passes the same authn/authz and rate limits as TCP TLS, since connection semantics differ.

**Why:** Middleboxes and legacy WAF rules keyed on TCP bypass QUIC entirely, giving attackers an unfiltered path to the origin.

**Detect:** `alt-svc: h3` advertised with no UDP firewall rules or QUIC-aware WAF; rate limiters bound to TCP sockets only.

**References:** RFC 9000, CWE-492, Cloudflare HTTP/3 deployment guidance

---

**Part of:** [api-design](../categories/api-design.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
