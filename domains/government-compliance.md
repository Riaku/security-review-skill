# government-compliance

Hardening baselines and regulatory regimes (CIS/STIG/FedRAMP/NIST/…).

## Detection signals

- compliance/ directory or FedRAMP/STIG/CIS/ITAR/CUI mentions in docs
- kube-bench, Lynis, Trivy misconfig, SCAP tooling configs
- Government/defense customer contracts or data marked CUI/ITAR

## Stack quick-map

- Any of the above → [hardening-benchmarks](../categories/hardening-benchmarks.md), [regulatory-frameworks](../categories/regulatory-frameworks.md)
- Federal cloud intent → [regulatory-frameworks](../categories/regulatory-frameworks.md) (FedRAMP, NIST 800-53)
- Health data → [regulatory-frameworks](../categories/regulatory-frameworks.md) (HIPAA) + [compliance-privacy](../categories/compliance-privacy.md)
