# Mutable Image Tags (latest) Instead of Digest Pinning

**SHOULD** reference images by immutable digest (`@sha256:`) rather than floating tags like `latest` in production manifests.

**Why:** A retagged or compromised `latest` silently changes what deploys, defeating rollback and supply-chain review.

**Detect:** Image fields ending in `:latest` or bare repo names; absence of `@sha256:` digest in Deployment/Pod specs.

**References:** CIS Docker 4.5, NIST SP 800-190 4.4, OWASP A08 Software Supply Chain, CWE-829
