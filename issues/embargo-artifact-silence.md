---
categories: [security-practices]
domains: [governance]
---

# Embargo Artifact Silence

**MUST** keep every artifact silent during a disclosure embargo: commit messages, branch names, release notes and CI job output.

**Why:** The advisory text is the last place a leak appears. A descriptive commit message or public CI log tells attackers what to exploit before a fix ships.

**Detect:** `git log --oneline` and branch names in the embargo window matching `CVE-`, `vuln`, `security fix` before the advisory is public.

**References:** Eclipse CSI Security Handbook: Embargoes, https://github.com/eclipse-csi/security-handbook/blob/main/docs/vulnerabilities/embargoes.md
