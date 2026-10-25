---
categories: [secrets-crypto, web-client-security]
domains: [frontend]
---

# Client-Bundle Secret Exposure

**MUST NOT** bake privileged credentials into browser-shipped bundles or the public build-time environment variables that inlining copies.

**Why:** Every value inlined at build time is readable by any visitor: a variable prefix is the only thing separating a server secret from a published one, and the built asset keeps the value after the source line is deleted.
**Detect:** grep source and build config for `NEXT_PUBLIC_`, `VITE_`, `REACT_APP_`, `EXPO_PUBLIC_` and `PUBLIC_` names carrying credential words, plus `DefinePlugin` and `import.meta.env`; then scan `dist/`, `build/` or `.next/static` for key-shaped strings and confirm each hit is non-privileged server-side.
**References:** OWASP Secrets Management Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html, CWE-798, https://cwe.mitre.org/data/definitions/798.html, Vite env and mode docs, https://vite.dev/guide/env-and-mode
