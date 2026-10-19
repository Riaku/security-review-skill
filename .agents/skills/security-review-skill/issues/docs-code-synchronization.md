---
categories: [documentation-quality]
domains: [backend]
---

# Docs-Code Synchronization

**MUST** update documentation in the same change that alters the behavior it describes; stale docs are treated as a bug, not a backlog item.

**Why:** Docs that lag code are actively harmful — users follow documented behavior that no longer exists, and security-relevant drift (auth steps, config keys) becomes a silent trap.

**Detect:** review PRs touching public behavior for corresponding doc updates; flag documented commands/config/APIs that no longer match code (run documented examples in CI where possible); check docs last-modified vs code churn on covered surfaces.

**References:** docs-as-code practice, Google style guide (keep docs current), CI doc-example testing (doctest/mddoc patterns)
