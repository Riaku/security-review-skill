---
categories: [web-client-security]
domains: [frontend]
---

# No Remote Code In Plugins

**MUST NOT** load executable code from remote origins into a privileged extension, plugin, or widget context; remote content is data only.

**Why:** Remote script inclusion hands code execution to whoever controls that path, inside a context that already holds elevated permissions.

**Detect:** grep extension manifests, plugin loaders, and CSP for remote script URLs (`<script src="https://`, `import("http`, `eval(fetch(`) and remote `script-src` allowances.

**References:** Remote JavaScript inclusion in browser extensions, https://arxiv.org/abs/2505.19456
