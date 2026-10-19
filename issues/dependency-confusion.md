---
categories: [supply-chain]
domains: [infrastructure]
---

# Dependency Confusion / Package-Name Squatting

**MUST NOT** resolve internal package names from public registries; private packages must install only from the internal registry via explicit scope or index pinning.

**Why:** Attackers publish an internal-named package with a higher version to npm/PyPI, and the resolver silently prefers it, executing attacker code at install time.

**Detect:** `.npmrc`/`pip.conf` without scoped `@internal:registry=`; `pip install` without `--index-url`; internal names absent from private registry listings.

**References:** CWE-427, OWASP A08:2021, Alex Birsan 2021 disclosure
