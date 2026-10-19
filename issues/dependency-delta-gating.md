---
categories: [supply-chain]
domains: [backend]
---

# Dependency Delta Gating

**SHOULD** evaluate dependency risk on the packages a change adds or upgrades, and report pre-existing findings separately.

**Why:** Blocking every pull request on the whole historical backlog trains teams to bypass the gate, while delta scoping keeps the check meaningful and actionable.

**Detect:** osv-scanner --lockfile=- <(git diff origin/main -- package-lock.json)  or an equivalent scan of base versus head lockfiles in the PR job

**References:** Dependency Review action, https://github.com/actions/dependency-review-action
