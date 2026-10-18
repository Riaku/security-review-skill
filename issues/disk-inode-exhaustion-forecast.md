# Disk and inode exhaustion forecasted with lead time

**MUST** forecast disk and inode consumption from historical growth rates and alert early enough (days, not hours) to act before full.

**Why:** A full disk or exhausted inode table corrupts writes and takes down every workload on the volume simultaneously, with no graceful degradation path.

**Detect:** grep monitoring for `disk_free_percent`, `inodes_free`, `predict_linear`/forecast queries in alert rules, log-rotation and cleanup cron jobs; flag alerts that fire only at >95% with no trend projection.

**References:** CWE-400, NIST SP 800-184, Google SRE monitoring four golden signals