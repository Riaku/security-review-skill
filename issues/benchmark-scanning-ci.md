# Benchmark Scanning in CI (kube-bench, Lynis, Trivy misconfig)

**SHOULD** run kube-bench, Lynis, or Trivy misconfig scans in CI on every image and host config change, failing the pipeline on high-severity findings.

**Why:** Hardening drifts silently after deploy; without automated benchmark gates, regressions ship unnoticed until an attacker exploits them.

**Detect:** Check `.github/workflows/*` or Jenkinsfile for `kube-bench`, `lynis audit`, `trivy config`, `trivy image --security-check misconfig` steps and severity gates.

**References:** CIS Benchmarks, NIST SP 800-53 CM-6, DevSecOps, CWE-1188

---

**Part of:** [cicd-pipeline-security](../categories/cicd-pipeline-security.md) · [hardening-benchmarks](../categories/hardening-benchmarks.md) · [infrastructure](../domains/infrastructure.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)
