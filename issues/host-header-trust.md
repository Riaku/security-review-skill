---
categories: [web-api-security]
domains: [backend]
---

# Host Header Trust

**MUST NOT** derive redirect targets, absolute URLs, cache keys, or access decisions from the client-supplied Host header.

**Why:** The Host header is attacker-controlled, so a trusted-host bug turns password-reset and OAuth flows into token exfiltration and poisons caches with the wrong origin. Configure the canonical host instead.

**Detect:** grep `request.host`, `X-Forwarded-Host`, `SERVER_NAME`, and `Host` reads inside URL builders; each must come from configuration, not the request.

**References:** Semgrep rule: request host used, https://github.com/semgrep/semgrep-rules/blob/develop/generic/nginx/security/request-host-used.yaml, CWE-346 Origin Validation Error
