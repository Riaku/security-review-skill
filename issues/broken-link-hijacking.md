---
categories: [supply-chain, web-client-security]
domains: [frontend, infrastructure]
---

# Broken Link & Dependency Hijacking

**SHOULD** remove or pin dead external references (deleted CDN packages, lapsed domains, 404'd script/CSS links) that attackers can register and serve malicious content through.

**Why:** A dangling `<script src>` to an unregistered domain is a supply-chain foothold the browser trusts implicitly — recon tools flag these by checking DNS on referenced hosts.

**Detect:** crawl pages and check HTTP status + DNS registration of every external script/CSS/frame host; grep templates for known-dead CDNs (bower, rawgit, shutdown libraries).

**References:** OWASP WSTG-BUSL, CWE-427, npm/CDN takeover incidents
