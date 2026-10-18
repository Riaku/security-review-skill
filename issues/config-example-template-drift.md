# Config-Example Template Drift

**SHOULD** keep a committed example config (`config.example.*`) listing every key the code reads, with the real config untracked — and verify in review that the example hasn't drifted from actual required keys.

**Why:** A stale example config is a trap: new deployers hit mysterious failures or silently miss security-relevant settings (TLS flags, auth toggles) that were added to code but never to the template.

**Detect:** diff example-config keys vs keys the code actually reads (grep config-access calls); flag example files missing entirely or missing recently-added settings; CI template-vs-code key comparison where tooling exists.

**References:** twelve-factor config separation, analysis-code config-template practice

---

**Part of:** [correctness-pitfalls](../categories/correctness-pitfalls.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
