---
categories: [security-practices]
domains: [governance]
---

# Specialist Reviewer Routing

**MUST** route changes touching security, privacy, or concurrency to a reviewer qualified in that domain instead of approving on trust.

**Why:** A generalist reviewer cannot tell a subtle authorization flaw from style, so approval becomes a formality that transfers the risk to users. Named ownership makes expertise a precondition of merge.

**Detect:** grep CODEOWNERS and branch-protection rules for security-sensitive paths (auth, crypto, payments, migrations) owned by a named team; unowned paths are the finding.

**References:** Google engineering practices: what to look for in a code review, https://github.com/google/eng-practices/blob/master/review/reviewer/looking-for.md
