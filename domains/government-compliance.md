# government-compliance

Hardening baselines and regulatory regimes (CIS/STIG/FedRAMP/NIST/…).

Detection signals:
- compliance/ directory or FedRAMP/STIG/CIS/ITAR/CUI mentions in docs
- kube-bench, Lynis, Trivy misconfig, SCAP tooling configs
- Government/defense customer contracts or data marked CUI/ITAR

Categories:
- `hardening-benchmarks`
- `regulatory-frameworks`

## Stack quick-map

- Any of the above → hardening-benchmarks, regulatory-frameworks
- Federal cloud intent → regulatory-frameworks (FedRAMP, NIST 800-53)
- Health data → regulatory-frameworks (HIPAA) + compliance-privacy
