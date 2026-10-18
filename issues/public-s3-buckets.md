---
categories: [cloud-network]
domains: [infrastructure]
---

# Public S3 Buckets

**MUST NOT** Any bucket holding application data, backups, or user content be publicly readable or writable; Block Public Access must be on at account and bucket level.

**Why:** Misconfigured ACLs and `Principal: "*"` policies are the most common cause of large-scale data leaks — and write-enabled buckets allow malware hosting or ransom via object overwrite.

**Detect:** Grep IaC for `acl = "public-read"` and `"Principal": "*"` with `s3:GetObject`/`PutObject`. Run `aws s3api get-public-access-block` per bucket; scan with Prowler or s3scanner. Watch for policies widening `Resource` beyond the intended prefix.

**Bad:**
```json
{ "Effect": "Allow", "Principal": "*", "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::prod-backups/*" }
```

**Good:**
```hcl
resource "aws_s3_bucket_public_access_block" "backups" {
  bucket = aws_s3_bucket.backups.id
  block_public_acls = true   ignore_public_acls = true
  block_public_policy = true restrict_public_buckets = true
}
```

**References:** CWE-284, CIS AWS Foundations 2.1.5, OWASP A01:2021 Broken Access Control, AWS S3 security best practices
