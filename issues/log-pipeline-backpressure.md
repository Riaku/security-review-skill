# Log Pipeline Backpressure and Drop Rate

**MUST** monitor the log pipeline's own backlog and drop rate under load so telemetry loss is visible when it happens.

**Why:** During an attack, log volume spikes exactly when you need it most; a silently dropping pipeline destroys evidence precisely then.

**Detect:** grep pipeline metrics for `dropped_total`, `rejected_batches`, `buffer_full`, agent `out_queue` depth; verify alerts on sustained drops > 0.

**References:** NIST SP 800-92, Vector/Fluent Bit drop metrics, Google SRE Workbook, CWE-770
