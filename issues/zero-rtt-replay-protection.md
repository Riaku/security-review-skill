---
categories: [web-api-security]
domains: [backend, infrastructure]
---

# 0-RTT Replay Protection

**MUST NOT** accept state-changing requests carried in TLS 1.3 0-RTT early data.

**Why:** An observer replays the early-data request verbatim, and the server performs the purchase, transfer, or deletion a second time.

**Detect:** grep for `ssl_early_data`, `early_data on`, and `Early-Data` handling, then confirm mutating methods are refused until the handshake completes.

**References:** NGINX Admin Handbook, https://github.com/trimstray/nginx-admins-handbook
