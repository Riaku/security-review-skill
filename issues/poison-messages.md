---
categories: [messaging-async]
domains: [data]
---

# Poison Messages

**MUST NOT** let a single malformed message crash or stall a consumer loop indefinitely; bound retries and eject it to quarantine.

**Why:** One crafted payload can halt an entire worker, turning a validation bug into a denial-of-service amplification vector.

**Detect:** grep consumer code for bare `except:` around handlers, missing `max_retries`, unbounded `while True: receive_message`, absent quarantine paths.

**References:** CWE-754, OWASP ASVS 5.1, AWS SQS poison pill guidance

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
