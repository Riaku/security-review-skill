---
categories: [supply-chain]
domains: [infrastructure]
---

# Dependency Version Cooldown

**SHOULD** delay adopting newly published dependency versions until a short cooldown period passes without incident.

**Why:** Malicious or broken releases are usually reported and yanked within days, while automated update bots consume them within hours. A cooldown converts someone else's incident into a version you never installed.

**Detect:** command: `npm config get minimum-release-age`, Renovate `minimumReleaseAge`, Dependabot `cooldown`, or the update bot's configured soak window in the automation config.

**References:** GitHub: the case for a cooldown before version updates, https://github.blog/security/supply-chain-security/the-case-for-a-cooldown-why-dependabot-now-waits-before-issuing-version-updates/
