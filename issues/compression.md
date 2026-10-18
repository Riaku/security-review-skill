# Compression

**SHOULD NOT** compress responses that contain attacker-controllable input alongside secrets in the same stream (CRIME/BREACH class).

**Why:** Adaptive compression of secrets with reflected input leaks tokens byte-by-byte through ciphertext length observations.

**Detect:** gzip/brotli on auth pages with CSRF tokens or API keys in body; `compression: true` with no secret-response exclusion.

**References:** CWE-310, CRIME (CVE-2012-4929), BREACH (CVE-2013-3587)

---

**Part of:** [api-design](../categories/api-design.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
