# MITRE ATT&CK Reference

Framework: https://attack.mitre.org/ (Enterprise matrix, Cloud matrix:
https://attack.mitre.org/matrices/enterprise/cloud/)

ATT&CK is used in this skill as the adversary-behavior backbone: detection
and threat-hunting items are written so findings can be tagged with tactic
IDs for SIEM mapping and coverage review.

## Tactic → our detection items

| ATT&CK tactic | Our issues |
|---|---|
| Initial Access (TA0001) | `exposed-data-service-ports`, `dependency-vulnerabilities`, `default-credentials`, `subdomain-takeover` |
| Execution (TA0002) | `ci-workflow-script-injection`, `os-command-injection`, `dynamic-code-evaluation`, `tool-argument-injection` |
| Persistence (TA0003) | `k8s-rbac-escalation-verbs`, `automount-serviceaccount-token`, `gitops-controller-cluster-admin-overreach` |
| Privilege Escalation (TA0004) | `vertical-privilege-escalation`, `container-escape-hardening`, `k8s-exec-attach-root-equivalent`, `cloud-privilege-escalation-paths` |
| Defense Evasion (TA0005) | `masquerading-detection`, `living-off-the-land`, `log-levels`, `push-protection` |
| Credential Access (TA0006) | `credential-access-detection`, `metadata-endpoint-credential-theft`, `imds-metadata-abuse`, `secrets-in-ci-logs`, `brute-force-protection` |
| Discovery (TA0007) | `sensitive-endpoint-exposure`, `forced-browsing-admin-panels`, `exposed-debug-actuator-endpoints` |
| Lateral Movement (TA0008) | `lateral-movement-detection`, `cross-account-role-confused-deputy`, `ssh-hardening` |
| Collection (TA0009) | `data-exfiltration-monitoring`, `pii-in-logs`, `excessive-data-exposure` |
| Command & Control (TA0011) | `beaconing-detection` |
| Exfiltration (TA0010) | `data-exfiltration-monitoring`, `egress-control` |
| Impact (TA0040) | `backup-verification-drills`, `poison-messages`, `wiper`-class runbooks via `incident-response` |

## Usage in reviews

- Tag each detection-type finding with the technique ID it maps to
  (e.g. `T1552.005 — credentials in cloud storage`) when the target org
  runs ATT&CK-mapped SIEM content.
- Coverage review: after a review, count which tactics have zero items
  exercised in the target's telemetry — that gap list is a detection-roadmap
  artifact.
- Threat modeling (Phase 1 of `threat-modeling`) should walk relevant
  tactics from the Cloud matrix for internet-facing systems.
