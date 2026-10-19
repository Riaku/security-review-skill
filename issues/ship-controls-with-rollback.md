---
categories: [deployment-release]
domains: [reliability]
---

# Ship Controls With Rollback

**MUST NOT** ship a security control that has no audit trail, no alerting on denial, and no tested way to disable it.

**Why:** An unobservable control cannot be shown to work or to have failed, and an unrollbackable one turns a bad launch into an outage.

**Detect:** grep the release for a kill switch or flag around the new check, an emitted `denied`/`blocked` event, and a rollback step in the runbook.

**References:** AWS Well-Architected Security Pillar, https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html
