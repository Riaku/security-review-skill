# Cloud IAM Privilege Escalation Paths

**MUST** trace every newly granted cloud permission for escalation edges before merge: actions that let a principal widen its own access.

**Why:** One overlooked `PassRole` or `AttachPolicy` grant turns a low-privilege service account into an administrator-in-waiting — the most common path from foothold to full account takeover.

**Detect:** In IAM JSON and IaC, look for `iam:PassRole`, `iam:AttachUserPolicy`, `iam:CreateAccessKey`, `iam:UpdateLoginProfile`, GCP `setIamPolicy`, and bindings referencing wildcards. Tools: Cloudsplaining, PMapper, IAM Access Analyzer.

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

**References:** CWE-269, MITRE ATT&CK T1548.005, Cloudsplaining, AWS IAM Security Best Practices
