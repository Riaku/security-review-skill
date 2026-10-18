# Admin Tasks as One-Off Processes from the Release

**SHOULD** run admin and maintenance tasks (migrations, REPLs, one-time scripts) as one-off processes from the same released code, config, and dependency isolation — committed to the repo — rather than ad-hoc scripts executed against production out-of-band.

**Why:** Out-of-band admin access (manual `psql` into prod, hand-copied scripts, SSH one-offs) is unauditable, drifts from the released code's assumptions, and is the classic vector for irreversible mistakes. Running the same image as a scoped one-off Job keeps credentials, code version, and audit trail aligned.

**Detect:** runbooks showing manual DB/console access instead of `kubectl job` or release-hook migrations; admin scripts not present in the repo; production mutations with no corresponding committed task definition.

**References:** 12factor.net/admin-processes, OWASP Logging Cheat Sheet (audit of admin actions), Kubernetes Jobs pattern
