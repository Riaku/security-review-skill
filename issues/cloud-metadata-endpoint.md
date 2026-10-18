---
categories: [cloud-network, web-api-security]
domains: [backend, infrastructure]
---

# Cloud Instance Metadata Endpoint Protection (IMDSv2)

**MUST** require session-token (IMDSv2) mode on every EC2-style instance and container host, with a hop limit of 1–2, so that simple single-request SSRF cannot read credentials.

**Why:** The original v1 metadata service answers any GET from the link-local address; an SSRF in user-facing code can then exfiltrate the instance's IAM role credentials in one request.

**Detect:** Review `aws ec2 modify-instance-metadata-options` settings, launch templates/user-data for `HttpTokens=required` and `HttpPutResponseHopLimit`, EKS nodegroup configs, and any Terraform `metadata_options` blocks left at defaults or `optional`.

**Bad:**
```hcl
metadata_options {
  http_tokens = "optional"   # v1 still reachable by plain GET SSRF
}
```

**Good:**
```hcl
metadata_options {
  http_tokens                 = "required"
  http_put_response_hop_limit = 1
}
```

**References:** AWS Security Bulletin IMPDS-2019-001, AWS Security Best Practices (SCA) SEC2-BP07, CIS AWS 5.6

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [web-api-security](../categories/web-api-security.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
