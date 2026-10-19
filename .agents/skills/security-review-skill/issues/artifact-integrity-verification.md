---
categories: [supply-chain]
domains: [infrastructure]
---

# Artifact Integrity Verification

**MUST** verify the checksum or signature of every downloaded artifact before executing it or shipping it onward.

**Why:** Transport security protects the channel, not the bytes: a compromised mirror or tampered upload serves whatever it chooses. Running or redistributing those bytes imports the attacker's code with your privileges.

**Detect:** grep download steps (`curl`, `wget`, `ADD <url>`, package-manager fetch hooks) for an adjacent `sha256sum -c`, `gpg --verify`, or `cosign verify`; flag any `curl ... | sh` and unverified `ADD` URL.

**References:** SLSA v1.0 requirements, https://slsa.dev/spec/v1.0/requirements, Codecov security update, https://about.codecov.io/blog/security-update/, CWE-494 Download of Code Without Integrity Check
