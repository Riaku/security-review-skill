---
categories: [documentation-quality]
domains: [backend]
---

# Comments Explain Why, Not What

**SHOULD** write comments that explain intent, rationale, and constraints — not restate what the code already says.

**Why:** What-comments duplicate the code, go stale on every edit, and crowd out the why-context that actually helps the next reader (and the security reviewer looking for the invariant).

**Detect:** flag comments that restate the adjacent line (`// increment counter` above `count++`); look for TODO/dead commented-out code left in; positive signal: comments citing constraints, bug IDs, invariants, spec sections.

**References:** Stack Overflow code-comment best practices, MIT CommKit coding-and-comment style, clean-code comment guidance

---

**Part of:** [documentation-quality](../categories/documentation-quality.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
