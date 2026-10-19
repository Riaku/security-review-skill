---
categories: [ai-llm]
domains: [backend]
---

# Adversarial Issue Descriptions

**MUST** treat issue and bug-report text that triggers automated code changes as untrusted input, and test the fixer with adversarially written issues.

**Why:** Whoever can author the work order can steer an auto-fixer toward code that passes the tests while removing a control.

**Detect:** grep for issue-triggered automation (`on: issues`, auto-fix labels, `@agent fix` handlers) and confirm each has an adversarial-description test case.

**References:** SWEADV (arXiv 2609.15963), https://arxiv.org/abs/2609.15963
