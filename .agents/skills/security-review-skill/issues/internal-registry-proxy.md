---
categories: [cicd-pipeline-security, supply-chain]
domains: [infrastructure]
---

# Internal Registry Proxy

**MUST** fetch dependencies through an internal registry or proxy that enforces allowlisting, malware blocking, and quarantine of new versions.

**Why:** Direct public-registry installs give every workstation and build job an unaudited path to arbitrary code. A proxy is the single choke point where policy applies and a bad version can be frozen.

**Detect:** command: `npm config get registry`, `pip config list`, `~/.m2/settings.xml`, and `.npmrc` mirror settings, plus the proxy's allowlist and quarantine policy in the platform repository.

**References:** GitHub: disrupting supply-chain attacks on npm and GitHub Actions, https://github.blog/security/supply-chain-security/disrupting-supply-chain-attacks-on-npm-and-github-actions/, NIST SP 800-161 supply chain risk management
