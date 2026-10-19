---
categories: [cloud-network, web-api-security]
domains: [backend, infrastructure]
---

# Relay Address Filtering

**MUST** block relaying or proxying to loopback, link-local, private, and reserved addresses on every supported address family, not only IPv4.

**Why:** A relay that will forward to an internal address is an open proxy into the private network, and IPv6 special ranges are routinely left unhandled.

**Detect:** grep relay/proxy config for peer or destination filtering (`no-multicast-peers`, denied CIDR lists, `allowed_peers`); check whether IPv6 ranges `::1`, `fc00::/7`, `fe80::/10` appear alongside the IPv4 denials.

**References:** OWASP ASVS v5.0 V17.1.1, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x26-V17-WebRTC.md, CWE-918
