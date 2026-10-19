---
categories: [ai-llm, cicd-pipeline-security]
domains: [governance, infrastructure]
---

# Unattended-Agent Automation Governance

**MUST** govern scheduled/event-triggered agents (cron, webhook) with: attribution to the automation creator, minimal tool surface per automation, trigger trust controls (signed webhooks, ignore non-trusted events), and preserved downstream human approval.

**Why:** Unattended agents run with no human per task, so every capability they hold is reachable from whatever triggers them; an automation must not inherit outbound authority from an inbound webhook or schedule it does not control.

**Detect:** automations with broad tool grants or opt-in to untrusted-user events; webhook endpoints accepting unsigned payloads; no owner attribution per automation; agent can merge/approve its own output.

**References:** GitHub Copilot coding agent risks and mitigations, OWASP LLM06:2025 Excessive Agency, NIST SP 800-53 AC-6
