---
categories: [mobile]
domains: [mobile]
---

# Mobile Reverse-Engineering & Tamper Protection

**SHOULD** detect rooted/jailbroken devices, debuggers, and repackaged builds, and gate high-risk features accordingly rather than trusting the client.

**Why:** Tampered clients bypass in-app restrictions, enabling fraud, license piracy, and automated abuse that server-side-only checks miss if nothing reports integrity.

**Detect:** grep `SafetyNet`/`Play Integrity`, `jailbreak`/`rootbeer`, `isDebuggerConnected`, `ptrace`, `frida`; verify Play Integrity / App Attest server-side validation exists.

**References:** OWASP MASVS-RESILIENCE-1..4, CWE-919, MAS Testing Guide Tampering and Reverse Engineering
