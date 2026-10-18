---
categories: [sre-incidents]
domains: [reliability]
---

# Runbooks

**MUST** keep remediation steps for every paged alert in a version-controlled runbook a non-author can execute.

**Why:** Alerts without written procedures route to Slack archaeology at 3 a.m. when the expert is unreachable.

**Detect:** `runbooks/` directory, alert annotations linking `runbook_url`, stale `last_reviewed` dates in frontmatter.

**References:** Google SRE Workbook (running incidents), NIST SP 800-61, PagerDuty runbook practices
