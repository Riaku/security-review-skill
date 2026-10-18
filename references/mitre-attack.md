# MITRE ATT&CK Reference

Framework: https://attack.mitre.org/ (Enterprise matrix, Cloud matrix:
https://attack.mitre.org/matrices/enterprise/cloud/)

ATT&CK is used in this skill as the adversary-behavior backbone: detection
and threat-hunting items are written so findings can be tagged with tactic
IDs for SIEM mapping and coverage review.

## Tactic → our detection items

| ATT&CK tactic | Our issues |
|---|---|
| Initial Access (TA0001) | [exposed-data-service-ports](../issues/exposed-data-service-ports.md), [dependency-vulnerabilities](../issues/dependency-vulnerabilities.md), [default-credentials](../issues/default-credentials.md), [subdomain-takeover](../issues/subdomain-takeover.md) |
| Execution (TA0002) | [ci-workflow-script-injection](../issues/ci-workflow-script-injection.md), [os-command-injection](../issues/os-command-injection.md), [dynamic-code-evaluation](../issues/dynamic-code-evaluation.md), [tool-argument-injection](../issues/tool-argument-injection.md) |
| Persistence (TA0003) | [k8s-rbac-escalation-verbs](../issues/k8s-rbac-escalation-verbs.md), [automount-serviceaccount-token](../issues/automount-serviceaccount-token.md), [gitops-controller-cluster-admin-overreach](../issues/gitops-controller-cluster-admin-overreach.md) |
| Privilege Escalation (TA0004) | [vertical-privilege-escalation](../issues/vertical-privilege-escalation.md), `container-escape-hardening`, [k8s-exec-attach-root-equivalent](../issues/k8s-exec-attach-root-equivalent.md), [cloud-iam-privilege-escalation](../issues/cloud-iam-privilege-escalation.md) |
| Defense Evasion (TA0005) | [masquerading-detection](../issues/masquerading-detection.md), [living-off-the-land](../issues/living-off-the-land.md), [log-levels](../issues/log-levels.md), `push-protection` |
| Credential Access (TA0006) | [credential-access-detection](../issues/credential-access-detection.md), [metadata-endpoint-credential-theft](../issues/metadata-endpoint-credential-theft.md), `imds-metadata-abuse`, [secrets-in-ci-logs](../issues/secrets-in-ci-logs.md), [brute-force-protection](../issues/brute-force-protection.md) |
| Discovery (TA0007) | [sensitive-endpoint-exposure](../issues/sensitive-endpoint-exposure.md), [forced-browsing-admin-panels](../issues/forced-browsing-admin-panels.md), [exposed-debug-actuator-endpoints](../issues/exposed-debug-actuator-endpoints.md) |
| Lateral Movement (TA0008) | [lateral-movement-detection](../issues/lateral-movement-detection.md), [cross-account-role-confused-deputy](../issues/cross-account-role-confused-deputy.md), [ssh-hardening](../issues/ssh-hardening.md) |
| Collection (TA0009) | [data-exfiltration-monitoring](../issues/data-exfiltration-monitoring.md), `pii-in-logs`, [excessive-data-exposure](../issues/excessive-data-exposure.md) |
| Command & Control (TA0011) | [beaconing-detection](../issues/beaconing-detection.md) |
| Exfiltration (TA0010) | [data-exfiltration-monitoring](../issues/data-exfiltration-monitoring.md), [egress-control](../issues/egress-control.md) |
| Impact (TA0040) | [backup-verification-drills](../issues/backup-verification-drills.md), [poison-messages](../issues/poison-messages.md), `wiper`-class runbooks via [incident-response](../issues/incident-response.md) |

## Usage in reviews

- Tag each detection-type finding with the technique ID it maps to
  (e.g. `T1552.005 — credentials in cloud storage`) when the target org
  runs ATT&CK-mapped SIEM content.
- Coverage review: after a review, count which tactics have zero items
  exercised in the target's telemetry — that gap list is a detection-roadmap
  artifact.
- Threat modeling (Phase 1 of [threat-modeling](../issues/threat-modeling.md)) should walk relevant
  tactics from the Cloud matrix for internet-facing systems.
