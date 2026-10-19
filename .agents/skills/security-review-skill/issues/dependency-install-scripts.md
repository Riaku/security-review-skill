---
categories: [supply-chain]
domains: [infrastructure]
---

# Dependency Install Scripts

**MUST** disable dependency install-time script execution in builds, enabling it only for explicitly reviewed packages that need it.

**Why:** Install hooks execute arbitrary code with the build's credentials before any scanner sees the package. A postinstall script is a complete compromise path that requires no vulnerability.

**Detect:** grep for `ignore-scripts=true` in `.npmrc`, `--ignore-scripts` on install commands, `postinstall`/`preinstall` keys in `package.json`, and `setup.py` execution or `--no-build-isolation` in Python builds.

**References:** OWASP NPM Security Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/NPM_Security_Cheat_Sheet.html
