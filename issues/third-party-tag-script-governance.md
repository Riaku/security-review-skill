---
categories: [third-party-integrations, web-client-security]
domains: [backend, frontend]
---

# Third-Party Tag & Script Governance

**MUST** inventory, approve, and CSP-restrict every third-party script loaded in the app (analytics, marketing tags, chat widgets).

**Why:** Marketing tags execute with your page's full privileges — a compromised tag is a Magecart-class supply-chain attack on your users' sessions and payment data.

**Detect:** list `<script src>` third-party hosts in templates; check CSP `script-src` uses nonces/hashes not `unsafe-inline`/wildcards; look for tag-manager sprawl without an approval list.

**References:** OWASP Magecart/Client-side supply chain, CSP script-src guidance, W3C CSP Level 3
