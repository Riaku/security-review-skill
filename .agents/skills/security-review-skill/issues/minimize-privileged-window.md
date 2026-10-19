---
categories: [authorization-access-control]
domains: [backend]
---

# Minimize the Privileged Window

**MUST** acquire elevated privilege as late as possible and drop it immediately after the operation that needs it completes.

**Why:** Every instruction executed while privileged is attack surface for that privilege, so a long window turns a small bug into a privileged one.

**Detect:** grep setuid/seteuid/setresuid sequences and privilege-drop calls, checking that privilege is released before the main loop

**References:** OWASP Go Secure Coding Practices, https://github.com/OWASP/Go-SCP
