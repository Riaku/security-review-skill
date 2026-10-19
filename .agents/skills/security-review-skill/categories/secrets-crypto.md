# secrets-crypto

Secrets handling and cryptographic primitives.

## What this category covers

This category covers anything secret or cryptographic: where credentials are stored and how they reach a running process, and whether the primitives protecting them are sound. The items span secret management and rotation, secret scanning and git-history remediation, and the many leakage paths — CI logs, Dockerfile layers and build args, Helm values, instance launch payloads, mobile binaries, IaC state, and committed .env files. They also cover encryption at rest and key custody; applied crypto such as password hashing and salting, weak primitives and modes, secure randomness for tokens, and client-side TLS verification; and the standards-driven cases: FIPS-validated modules and approved signatures, post-quantum migration and crypto-agility, and long-lived data exposed to later decryption. Expect findings that describe a secret exposed where it should not be, or crypto applied with a broken primitive, a missing check, or a key nobody rotates.

- Secret storage and sourcing: secret managers, rotation automation, and centralization of integration and pipeline credentials.
- Leakage paths: CI logs, Dockerfile layers and build args, Helm values, launch payloads, mobile binaries, IaC state, and committed .env files.
- Detection and remediation: secret scanning, git-history rewriting, and verification that a leaked credential was actually revoked.
- Password and credential hashing: per-password salting, bcrypt or Argon2 parameters, and hashing rather than reversible encryption.
- Cryptographic primitives: weak ciphers and modes, encryption at rest, secure token randomness, and client-side TLS verification.
- Standards-driven crypto: FIPS-validated modules and signatures, post-quantum migration and crypto-agility, and long-lived data exposed to later decryption.

## What it does not cover

- [authentication](../categories/authentication.md) — login, session, and token lifecycle belong there, even though credentials feed it.
- [cicd-pipeline-security](../categories/cicd-pipeline-security.md) — pipeline execution, runner hardening, and artifact integrity belong there beyond the secrets that flow through them.
- [containers-k8s](../categories/containers-k8s.md) — cluster and workload configuration belongs there, even when a secret is stored in that configuration.
- [supply-chain](../categories/supply-chain.md) — dependency and artifact provenance belong there rather than key material.

## What a finding here looks like

- A private key committed to the repo and left in history, so a fresh clone still contains it.
- A live API key echoed into CI output because a debug step dumped the environment.
- Secrets copied into an image layer with COPY or ARG, recoverable from the image's layer history.
- A password store using reversible encryption or a bare fast hash instead of a salted one-way hash.
- An outbound TLS client with certificate or hostname verification disabled in production.
