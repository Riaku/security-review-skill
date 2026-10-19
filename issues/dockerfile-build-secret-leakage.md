---
categories: [cicd-pipeline-security, secrets-crypto]
domains: [backend, infrastructure]
---

# Dockerfile Secret Leakage via COPY, Build Args, and Cache Layers

**MUST NOT** bake secrets into images via `COPY` of credential files or plain `ARG`/`ENV` values; use BuildKit `--mount=type=secret` instead.

**Why:** Copied files and build args persist in the final image: copied file contents remain in the saved layers of any pushed image, and ARG/ENV values stay visible in `docker history` and image metadata.

**Detect:** Grep Dockerfiles for `COPY .npmrc`, `COPY *credentials*`, `ARG API_KEY`, `ENV SECRET`, or `RUN ... $ARG` patterns; inspect `docker history` for leaked values.

**References:** OWASP Docker Top 10 D06 (Protect Secrets), CWE-540, NIST SP 800-218 (SSDF), BuildKit secret mounting docs, Trivy secret scanning / Checkov Dockerfile checks
