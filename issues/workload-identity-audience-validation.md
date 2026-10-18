---
categories: [authentication, cloud-network]
domains: [backend, infrastructure]
---

# Workload Identity / IRSA Audience and Claim Validation Gaps

**MUST** validate the audience (`aud`) and issuer (`iss`) claims on every federated workload token and scope each identity to the single service it is meant to reach.

**Why:** If a token minted for service A is accepted by service B without audience checks, any workload holding the weaker token can impersonate the stronger one — cross-service confusion that bypasses IAM entirely.

**Detect:** In STS `AssumeRoleWithWebIdentity` trust policies, check `Condition.StringEquals` on `token.actions.githubusercontent.com:aud` and `:sub` (repo + ref, not just `repo:*`). For SPIFFE/IRSA reviews, look for trust policies matching only the issuer URL with no audience or subject constraints, and app code that skips `aud` verification in JWT libraries (`verify_aud=False`).

**Bad:**
```json
"Condition": {"StringEquals": {
  "token.actions.githubusercontent.com:iss": "https://token.actions.githubusercontent.com"}}
```

**Good:**
```json
"Condition": {"StringEquals": {
  "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
  "token.actions.githubusercontent.com:sub": "repo:acme/deploy:ref:refs/heads/main"}}
```

**References:** CWE-287, OWASP ASVS 3.5, AWS IRSA trust policy docs, SPIFFE/SPIFFI threat model
