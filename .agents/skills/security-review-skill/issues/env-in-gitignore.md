---
categories: [secrets-crypto]
domains: [backend]
---

# .env in .gitignore

**MUST** list `.env`, `.env.*` (except committed `.env.example` templates) in `.gitignore` so local configuration never enters version control.

**Why:** A single committed `.env` exposes database URLs, API keys, and session secrets to everyone with repo read access, including forks.

**Detect:** `git check-ignore -v .env`; missing `.env` entry in `.gitignore`; `git ls-files | grep '\.env$'`.

**References:** OWASP Top 10 A05:2021, CWE-538, CWE-312
