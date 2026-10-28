---
categories: [compliance-privacy, web-client-security]
domains: [frontend, governance]
---

# Third-Party Subresource Hosting

**MUST** self-host or proxy the static subresources served directly to users' browsers — web fonts, JavaScript and CSS libraries — rather than hot-linking a third-party CDN.

**Why:** Every hot-linked request discloses the visitor's IP address and user-agent to the third-party host, a personal-data transfer to a party the visitor never chose; a Munich court awarded a visitor damages over a Google Fonts call alone.
**Detect:** grep templates and stylesheets for `fonts.googleapis.com`, `fonts.gstatic.com`, `cdnjs.cloudflare.com`, `unpkg.com`, `ajax.googleapis.com`; confirm each host is replaced by a self-hosted or same-origin proxy copy.
**References:** GDPR Arts. 44–49, https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679, CJEU C-582/14 (dynamic IP addresses as personal data)
