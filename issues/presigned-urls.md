---
categories: [cloud-network]
domains: [infrastructure]
---

# Presigned URLs

**SHOULD** Presigned URLs carry the shortest expiry the user journey tolerates — minutes, not days — and MUST NOT be generated for destructive or administrative operations.

**Why:** A presigned URL is a bearer credential: anyone holding it bypasses IAM entirely, and links pasted into chats, logs, and Referer headers keep working long after the session ends.

**Detect:** Grep for `generate_presigned_url`, `sign_url`, `X-Amz-Expires` and audit the expiry values — anything above 15 minutes needs justification. Check whether logs record full signed URLs, and whether any flow presigns `DeleteObject`/`PutObject`.

**Bad:**
```python
url = s3.generate_presigned_url("get_object",
        Params={"Bucket": b, "Key": k}, ExpiresIn=60*60*24*7)  # 7 days
```

**Good:**
```python
url = s3.generate_presigned_url("get_object",
        Params={"Bucket": b, "Key": k}, ExpiresIn=300)  # 5 minutes
```

**References:** AWS S3 presigned URL best practices, CWE-539, OWASP A07:2021

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
