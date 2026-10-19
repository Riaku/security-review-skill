---
categories: [email-security]
domains: [infrastructure]
---

# Forwarded Mail Authentication

**MUST** treat SPF as void for relayed mail and require a DKIM signature that survives forwarding before trusting the sender identity.

**Why:** Forwarding services re-send mail from their own infrastructure, so an SPF pass at the receiver describes the relay rather than the author, and attackers use that gap to spoof well-protected domains.

**Detect:** grep mail-filter and anti-phish config for an auth decision on `spf=pass` alone, `Authentication-Results` parsed without `dkim=pass`, and forwarder rewrites (`SRS`, `.forward`).

**References:** Forwarding breaks anti-spoofing assumptions, https://arxiv.org/abs/2302.07287, RFC 7208 (SPF), RFC 6376 (DKIM)
