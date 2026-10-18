---
categories: [cicd-pipeline-security, secrets-crypto]
domains: [backend, infrastructure]
---

# Dockerfile Secret Leakage via COPY, Build Args, and Cache Layers

**MUST NOT** bake secrets into images via `COPY` of credential files or plain `ARG`/`ENV` values; use BuildKit `--mount=type=secret` instead.

**Why:** Copied files and build args persist in layer history and are recoverable from any pushed image with `docker history`.

**Detect:** Grep Dockerfiles for `COPY .npmrc`, `COPY *credentials*`, `ARG API_KEY`, `ENV SECRET`, or `RUN ... $ARG` patterns; inspect `docker history` for leaked values.

**References:** OWASP Docker DS02, CWE-540, NIST SP 800-218 (SSDF), BuildKit secret mounting docs, hadolint DL3025/DL3009

---

**Part of:** [cicd-pipeline-security](../categories/cicd-pipeline-security.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
