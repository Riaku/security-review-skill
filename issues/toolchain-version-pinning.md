---
categories: [supply-chain]
domains: [backend, infrastructure]
---

# Pinned Toolchain Versions

**MUST** pin the runtime and build-toolchain versions in repository files that CI and local builds both read, rather than a floating `latest`.

**Why:** A floating runtime silently changes the compiler, linker and standard library between builds, so a passing pipeline proves nothing about the next one and a compromised toolchain release arrives without a commit.
**Detect:** look for `.nvmrc`, `.python-version`, `rust-toolchain.toml`, `mise.toml`, `.tool-versions` or `engines` at the repo root and check CI reads it; flag `node-version: lts/*`, an unversioned `rustup default stable`, or a build image tagged `latest`.
**References:** Reproducible Builds project, https://reproducible-builds.org/, NIST SP 800-218, https://csrc.nist.gov/pubs/sp/800/218/final, SLSA specification, https://slsa.dev/spec/v1.1/
