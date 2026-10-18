# Broken Link & Dependency Hijacking

**SHOULD** remove or pin dead external references (deleted CDN packages, lapsed domains, 404'd script/CSS links) that attackers can register and serve malicious content through.

**Why:** A dangling `<script src>` to an unregistered domain is a supply-chain foothold the browser trusts implicitly — recon tools flag these by checking DNS on referenced hosts.

**Detect:** crawl pages and check HTTP status + DNS registration of every external script/CSS/frame host; grep templates for known-dead CDNs (bower, rawgit, shutdown libraries).

**References:** OWASP WSTG-BUSLOGIC broken-link hijacking, CWE-427, npm/CDN takeover incidents

---

**Part of:** [supply-chain](../categories/supply-chain.md) · [web-client-security](../categories/web-client-security.md) · [frontend](../domains/frontend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
