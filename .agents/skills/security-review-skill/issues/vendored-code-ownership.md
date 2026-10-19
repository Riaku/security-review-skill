---
categories: [supply-chain]
domains: [governance]
---

# Vendored Code Ownership

**MUST** assign a named owner and a documented upstream-fix process to every vendored or forked dependency before it enters the tree.

**Why:** A vendored copy stops receiving fixes the moment it is copied, yet it still looks like a normal dependency in the manifest. The fork becomes permanent unpatched surface that no scanner attributes to you.

**Detect:** judgment: `vendor/`, `third_party/`, and submodule trees, matched against CODEOWNERS and a documented patch or upgrade path for each.

**References:** NIST SP 800-218 (SSDF) PW.4, OpenSSF Concise Guide for Developing More Secure Software, https://github.com/ossf/wg-best-practices-os-developers/blob/main/docs/Concise-Guide-for-Developing-More-Secure-Software.md
