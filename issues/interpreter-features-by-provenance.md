---
categories: [mobile]
domains: [mobile]
---

# Interpreter Features by Provenance

**MUST** enable script interpreters in embedded webviews only for content the app fully controls, never for remote or user content.

**Why:** A JavaScript bridge in a webview exposes native capabilities to whatever page loads. One redirect or injected frame turns the bridge into remote code execution.

**Detect:** `setJavaScriptEnabled(true)`, `addJavascriptInterface(` or `setAllowFileAccess(true)` next to a load of a remote URL.

**References:** JSSEC Android Secure Coding Guide, https://www.jssec.org/dl/android_securecoding_en.pdf
