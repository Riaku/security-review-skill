---
categories: [security-practices]
domains: [backend]
---

# Sandbox Untrusted Code

**MUST** run plugins, user scripts, and third-party extensions with no ambient authority: no filesystem, network, or credentials unless explicitly granted.

**Why:** Third-party code runs with the host process's identity, so one malicious plugin has exactly the access the service has.

**Detect:** grep plugin and eval loaders (`vm.runInNewContext` presented as a sandbox, `importlib`, `eval`, dynamic `require`) for filesystem, network, and env access in the same context.

**References:** Node.js security guidance, https://nodejs.org/en/about/security, OWASP Deserialization Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html
