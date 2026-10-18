---
categories: [cicd-pipeline-security, secrets-crypto]
domains: [backend, infrastructure]
---

# Secrets in CI Logs

**MUST NOT** echo, print, or interpolate secrets into CI output; mask values via CI secret masking and avoid commands that dump environment variables.

**Why:** Build logs are widely readable — teammates, forked PRs, and third-party integrations can harvest tokens from a single verbose step.

**Detect:** `echo $SECRET`, `set -x` in steps handling credentials, `env`/`printenv` in pipelines, `export` of tokens without `::add-mask::`.

**References:** OWASP ASVS V2.10.3, CWE-532, CWE-214

---

**Part of:** [cicd-pipeline-security](../categories/cicd-pipeline-security.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
