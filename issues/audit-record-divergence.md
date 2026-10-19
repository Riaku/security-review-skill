---
categories: [observability]
domains: [backend]
---

# Action-to-Audit Divergence Checks

**MUST** test each class of divergence between an executed action and its audit record before treating the log as evidence of what happened.

**Why:** Aggregate logging records what the system claims happened, not whether it matched the approval; action-without-approval, approval-without-action, silent failure logged as success, and wrong-target execution each need their own structural check.

**Detect:** judgment: the audit design and the checker wired to each of the four divergence classes

**References:** Architectural Obsolescence of Unhardened Agentic-AI Runtimes, https://arxiv.org/abs/2605.01740
