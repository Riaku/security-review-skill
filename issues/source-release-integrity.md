---
categories: [supply-chain]
domains: [infrastructure]
---

# Source Release Integrity

**MUST** publish source packages containing only version-controlled content, and require consumers to build generated artifacts themselves.

**Why:** A pre-generated file shipped inside a source tarball is trusted by everyone who installs it and verified by nobody. Building from source in the consumer's pipeline removes that unearned trust.

**Detect:** command: `npm pack --dry-run`, `tar -tzf dist/*.tar.gz`, or `python -m build --sdist` inspected for generated artifacts (compiled binaries, bundled output) absent from the repository.

**References:** OpenSSF Concise Guide for Developing More Secure Software, https://github.com/ossf/wg-best-practices-os-developers/blob/main/docs/Concise-Guide-for-Developing-More-Secure-Software.md, SLSA v1.0 requirements
