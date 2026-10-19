---
categories: [secrets-crypto]
domains: [infrastructure]
---

# Secrets Not in Arguments

**MUST NOT** pass secrets as command-line arguments, where process listings, shell history, and crash reports expose them.

**Why:** Arguments are visible in `ps`, `/proc`, shell history, and crash dumps, and child processes inherit them. A secret on a command line is disclosed to every local user before the command finishes.

**Detect:** grep for `--password`, `--token`, `-p$`, `mysql -p...`, `curl -u user:pass`, and secret values interpolated into `subprocess`/`exec` argument lists.

**References:** OWASP Secrets Management Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html, CWE-214 Invocation of Process Using Visible Sensitive Information
