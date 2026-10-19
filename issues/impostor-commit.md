---
categories: [supply-chain]
domains: [infrastructure]
---

# Commit in Trusted Repository

**MUST** resolve a pinned commit against the trusted repository itself before executing it, not merely accept that the hash is reachable through a fork network.

**Why:** Fork networks let a commit with an identical hash live in an attacker's repository, so a pinned SHA can name code you never reviewed.

**Detect:** gh api repos/OWNER/REPO/commits/SHA and confirm the returned html_url is the trusted repository

**References:** zizmor, https://github.com/zizmorcore/zizmor
