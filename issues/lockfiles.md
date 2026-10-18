# Lockfiles

**MUST** commit and honor dependency lockfiles so every install resolves to identical, audited versions.

**Why:** Unpinned resolution lets a transitive dependency change silently between builds, opening the door to typosquat and version-rollback attacks.

**Detect:** Missing `package-lock.json`, `poetry.lock`, `go.sum`; CI flags like `--no-lock`, `npm install` without `ci`; `.gitignore` excluding lockfiles.

**References:** OWASP A06:2021, CWE-829, SCB-002
