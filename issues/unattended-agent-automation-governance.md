# Unattended-Agent Automation Governance

**MUST** govern scheduled/event-triggered agents (cron, webhook) with: attribution to the automation creator, minimal tool surface per automation, trigger trust controls (signed webhooks, ignore non-trusted events), and preserved downstream human approval.

**Why:** Unattended agents run with no human per task — GitHub documents a dedicated automations-risk section; DeepSeek's review harness gives inbound webhook auth ZERO outbound authority by design.

**Detect:** automations with broad tool grants or opt-in to untrusted-user events; webhook endpoints accepting unsigned payloads; no owner attribution per automation; agent can merge/approve its own output.

**References:** GitHub Copilot automations risks-and-mitigations, DeepSeek harness webhook model, Cursor Automations docs

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [cicd-pipeline-security](../categories/cicd-pipeline-security.md) · [infrastructure](../domains/infrastructure.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
