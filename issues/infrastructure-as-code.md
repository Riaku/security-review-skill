---
categories: [deployment-release]
domains: [infrastructure]
---

# Infrastructure as Code

**MUST** define all cloud and cluster resources in version-controlled IaC templates reviewed through pull requests, never via console clicks.

**Why:** Manually created resources drift from policy, escape security review, and cannot be audited or reproducibly rebuilt after compromise.

**Detect:** grep for open security group ingress (`cidr_blocks = ["0.0.0.0/0"]`), unencrypted storage flags, and console-created resources flagged by drift detection.

**References:** AWS Config drift detection, CIS AWS 5.4, IaC Scanning OWASP, Checkov/tfsec baselines
