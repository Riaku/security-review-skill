---
categories: [web-api-security]
domains: [backend]
---

# Forced Browsing & Unprotected Admin Panels

**MUST** authenticate and network-restrict every admin panel, dashboard, and management UI (Kibana, Adminer, /admin, wp-admin, portainer, argocd guest access).

**Why:** Scanners (Nuclei, ffuf) find default-open admin UIs constantly; "security by obscure path" fails against wordlist enumeration.

**Detect:** fuzz paths `/admin`, `/console`, `/kibana`, `/portainer`, `/adminer`; check Nginx/ingress auth annotations and network policies for management routes.

**References:** OWASP WSTG-ATHZ-02, MITRE ATT&CK T1595.001, Nuclei admin-panel templates
