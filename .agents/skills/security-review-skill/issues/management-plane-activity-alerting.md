---
categories: [cloud-network, observability]
domains: [infrastructure, reliability]
---

# Management-Plane Activity Alerting

**MUST** route cloud control-plane audit streams (CloudTrail, Azure Activity Log, GCP Cloud Audit Logs) into real-time metric filters and alarms so privileged API activity — root/console usage, security-group and firewall changes, IAM policy modifications, key deletion — pages a human within minutes instead of waiting for a periodic log review.

**Why:** Audit logs that only get read quarterly turn a live intrusion into a post-mortem; attackers mutate security groups and IAM grants in hours, and the provider's control-plane API leaves no trace in workload telemetry. Alerting is the difference between catching a stolen-credential session mid-flight and discovering it next quarter.

**Detect:** CloudTrail configured with CloudWatch metric filters + alarms (or equivalent GuardDuty/Activity Log alert rules) covering: root account usage, `AuthorizeSecurityGroupIngress` widening, `iam:Put*Policy`/`Attach*Policy`, console login failures burst, KMS key scheduling-for-deletion; absence of any alarm wired to the audit stream is the finding. Distinguish from `admin-activity-review` (periodic human review) — this item requires automated real-time alerting.

**References:** CIS AWS 3.x (CloudTrail processing & alerting), AWS CloudTrail best practices, Azure Activity Log alert guidance, aquasecurity/trivy-checks AWS CloudTrail alert rules
