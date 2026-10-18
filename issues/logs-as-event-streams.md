# Logs as Event Streams

**SHOULD** write the log stream unbuffered to stdout/stderr and leave routing, aggregation, and retention to the execution environment; **SHOULD NOT** write or manage logfiles from inside a container.

**Why:** App-managed logfiles inside containers silently fill ephemeral storage (triggering node eviction), lose evidence on restart (breaking incident forensics), and bypass the centralized pipeline where PII-scrubbing and retention policy live.

**Detect:** log file paths or rotating file handlers in app config inside containerized deploys; missing stdout logger configuration; container logs empty despite active logging code.

**References:** 12factor.net/logs, OWASP Logging Cheat Sheet, Kubernetes logging best practices
