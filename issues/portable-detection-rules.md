---
categories: [observability]
domains: [infrastructure]
---

# Portable Detection Rules

**MUST** author detection logic in a vendor-neutral, machine-readable rule format that compiles to each backend's query dialect, keeping native queries out of the source of truth.

**Why:** Detection knowledge locked in one query dialect cannot be peer-reviewed, tested elsewhere, or migrated without rewriting the entire detection program.

**Detect:** grep rule files for native query syntax (index=, sourcetype=, EventID) where a neutral schema (logsource, detection, selection) is expected

**References:** Sigma, https://github.com/SigmaHQ/sigma, Agent Threat Rules, https://github.com/Agent-Threat-Rule/agent-threat-rules
