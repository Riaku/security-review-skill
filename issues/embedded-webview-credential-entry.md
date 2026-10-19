---
categories: [authentication]
domains: [frontend, mobile]
---

# Embedded WebView Credential Entry

**MUST NOT** collect credentials inside a webview or embedded browser owned by another application; use the platform browser or the system authentication API.

**Why:** The host application can record every keystroke, auto-submit the form, and read the session cookie, so the credential is disclosed to a party the identity provider never authorized.

**Detect:** grep for `WebView`, `WKWebView`, `webview_flutter`, or `WebViewClient` loading an authorization or login URL.

**References:** RFC 8252 OAuth 2.0 for Native Apps, https://www.rfc-editor.org/rfc/rfc8252.html
