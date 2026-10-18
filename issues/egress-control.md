# Egress Control (outbound traffic allow-listed; exfil paths narrowed)

**SHOULD** restrict outbound network traffic to an explicit allow-list so compromised hosts cannot freely phone home or exfiltrate data.

**Why:** Default-open egress is the exfiltration highway: malware, reverse shells, and data staging all depend on reaching arbitrary external endpoints.

**Detect:** grep egress configs: `NetworkPolicy egress`, `egress gateway`, `egress_filter`, proxy allow-lists, `default-deny` outbound firewall rules, `egress-destination-range`.

**References:** NIST SP 800-207 Zero Trust, CIS Control 12, MITRE ATT&CK TA0011 (Exfiltration), CIS Kubernetes Benchmark 5.3
