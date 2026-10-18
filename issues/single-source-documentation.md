# Single-Source Documentation

**SHOULD** document each fact once with links pointing at the canonical location, rather than repeating it across files.

**Why:** Every duplicate is a future contradiction — copies drift out of sync and readers can't tell which one is current; the fix cost multiplies with each copy made.

**Detect:** grep docs for the same instructions/config/versions appearing in multiple files; flag copy-pasted blocks; check cross-references use links/includes instead of duplication.

**References:** Write the Docs DRY documentation guidance, docs-as-code single-source practice

---

**Part of:** [documentation-quality](../categories/documentation-quality.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
