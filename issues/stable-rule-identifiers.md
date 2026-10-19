---
categories: [observability]
domains: [infrastructure]
---

# Stable Rule Identifiers

**MUST** give every detection rule an immutable identifier under a versioned rule schema, keeping severity, category, and owner in separate mutable metadata fields.

**Why:** Rules are cited by incident reports and dashboards, so reassigned or meaning-laden identifiers break references and turn wrong the moment classification changes.

**Detect:** grep -h '^id:' rules/*.yml | sort | uniq -d  (duplicate or reassigned IDs), plus a schema-version field in each rule header

**References:** Agent Threat Rules, https://github.com/Agent-Threat-Rule/agent-threat-rules
