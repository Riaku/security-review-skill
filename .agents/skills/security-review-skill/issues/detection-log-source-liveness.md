---
categories: [observability]
domains: [infrastructure]
---

# Detection Log-Source Liveness

**MUST** verify that every deployed detection rule's declared log source is actually arriving, and alert on rules that have received no events.

**Why:** A rule whose index or channel is never populated is a control that silently does not exist while counting as deployed coverage.

**Detect:** query the backend for the newest event per log source (tstats latest(_time) by index, or SELECT max(ts) GROUP BY source) and compare with each rule's logsource

**References:** deadair, https://github.com/alephnull-sh/deadair
