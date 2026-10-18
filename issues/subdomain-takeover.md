# Subdomain Takeover / Dangling DNS

**MUST NOT** Any DNS record remain pointing at a deprovisioned cloud resource — S3 bucket, Heroku app, CloudFront distribution — after that resource is released.

**Why:** A CNAME to a vacant target is a claim ticket: an attacker registers it under their own account and instantly serves arbitrary content, sets cookies, and harvests credentials on your trusted domain.

**Detect:** Enumerate A/CNAME records and probe targets for "not found" signatures: `NoSuchBucket`, Heroku "No such app", GitHub Pages 404. Diff DNS against live provisioned resources in CI; flag records for retired campaigns and expired vendor trials.

**Bad:**
```
marketing.example.com.  CNAME  old-campaign.s3-website-us-east-1.amazonaws.com
# bucket deleted; attacker creates it and pages on your domain
```

**Good:**
```
# CI check: every CNAME target must exist and be org-owned,
# or the record fails the pipeline and gets removed
```

**References:** OWASP WSTG-CONF-10 (Subdomain Takeover), HackerOne takeover methodology, Can-I-Takeover-it project
