---
categories: [web-client-security]
domains: [frontend, mobile]
---

# Clipboard Data Exposure

**MUST** suppress copy, cut, and drag for displayed secrets and personal data, and prefer in-app transfer paths over shared OS buffers.

**Why:** Clipboard, drag-drop, and share buffers are readable by every process on the machine and can persist after the user leaves the screen.

**Detect:** grep navigator.clipboard.writeText, ClipboardManager, UIPasteboard.general, NSPasteboard near token, password, or PII handlers

**References:** Android Secure Coding Guide, https://www.jssec.org/dl/android_securecoding_en_20250827.pdf
