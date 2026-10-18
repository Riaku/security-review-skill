# Cloud metadata service abuse (SSRF to IMDS, IMDSv2 enforcement, metadata blocking)

**MUST** combine defenses against metadata abuse end-to-end: enforce IMDSv2 hop-limit 1 on instances, deny link-local egress from SSRF-capable workloads, and reject user-supplied URLs that resolve into reserved ranges at connect time.

**Why:** Metadata abuse rarely needs a novel exploit — an attacker chains an ordinary SSRF with a v1-tolerant instance or an open egress path, and walks away with node role credentials. Any single missing layer in the chain is enough to complete the attack.

**Detect:** Verify `HttpTokens=required` plus `HttpPutResponseHopLimit=1` on launch templates; confirm egress proxies/NetworkPolicies drop `169.254.169.254` and cloud aliases; test SSRF filters with decimal (`2852039166`), IPv6-mapped, and DNS-rebind forms. Review container hostNetwork settings that sidestep pod-level blocks.

**Bad:**
```python
# SSRF filter checks the string only; v1 IMDS answers a plain GET
if not url.startswith("http://169.254.169.254"):
    requests.get(url)
```

**Good:**
```
# defense in depth: v2-only IMDS + network-level deny
aws ec2 modify-instance-metadata-options --instance-id i-123 \
  --http-tokens required --http-put-response-hop-limit 1
iptables -t nat -A OUTPUT -d 169.254.169.254 -j REJECT
```

**References:** AWS IMDSv2 security bulletin, CIS AWS 5.6/5.7, OWASP SSRF Prevention Cheat Sheet, MITRE ATT&CK T1552.005
