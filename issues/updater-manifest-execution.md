---
categories: [supply-chain]
domains: [infrastructure]
---

# Updaters Must Not Execute Manifests

**MUST NOT** allow a dependency updater to execute install or setup scripts from the dependencies it processes.

**Why:** Install and setup scripts in a freshly updated dependency run with the updater's credentials, turning an update into code execution.

**Detect:** grep insecure-external-code-execution or --allow-exec flags in updater configuration

**References:** zizmor, https://github.com/zizmorcore/zizmor
