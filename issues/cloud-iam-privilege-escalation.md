---
categories: [authorization-access-control, cloud-network]
domains: [backend, infrastructure]
---

# Cloud IAM Privilege Escalation Paths

**MUST** trace every newly granted cloud permission for escalation edges before merge: actions that let a principal widen its own access.

**Why:** One overlooked `PassRole` or `AttachPolicy` grant turns a low-privilege service account into an administrator-in-waiting — the most common path from foothold to full account takeover. Escalation rarely arrives as one obvious admin grant; it hides in combinations (PassRole plus a role that trusts you, or a wildcard that later resolves to a new powerful action), so the diff must be judged against what the principal already holds.

**Detect:** In IAM JSON and IaC, look for `iam:PassRole`, `iam:AttachUserPolicy`, `iam:CreateAccessKey`, `iam:UpdateLoginProfile`, GCP `setIamPolicy`, and bindings referencing wildcards; check whether managed-policy attachments or GCP folder/organization inheritance silently widen the effective set, and whether any `NotAction` or `Resource: "*"` will be inherited by future service launches. Tools: Cloudsplaining, PMapper, IAM Access Analyzer — diff the reachable-permissions graph before/after the change. Periodically recompute the full role-to-role and cross-account escalation graph and prune every path from low privilege to admin.

**Bad:**
```json
{"Effect": "Allow", "Action": ["iam:AttachRolePolicy", "iam:PassRole"], "Resource": "*"}
```

**Good:**
```json
{"Effect": "Allow", "Action": "iam:PassRole",
 "Resource": "arn:aws:iam::111122223333:role/deploy-app",
 "Condition": {"StringEquals": {"iam:PassedToService": "lambda.amazonaws.com"}}}
```

**References:** CWE-269, MITRE ATT&CK T1548.005, Cloudsplaining, AWS IAM Security Best Practices, GCP Policy Analyzer

---

**Part of:** [authorization-access-control](../categories/authorization-access-control.md) · [cloud-network](../categories/cloud-network.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
