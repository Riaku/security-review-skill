---
categories: [correctness-pitfalls]
domains: [backend]
---

# No I/O Under Lock

**MUST NOT** hold a lock, transaction, or connection across network calls, disk I/O, or any operation with unbounded latency.

**Why:** One slow dependency then stalls every caller waiting on the lock, turning a latency blip into a system-wide outage.

**Detect:** grep lock scopes (`synchronized`, `with lock:`, `SELECT ... FOR UPDATE`, `BEGIN`) that enclose HTTP clients, file reads, or message publishes.

**References:** SEI CERT Oracle Coding Standard for Java, https://wiki.sei.cmu.edu/confluence/display/java/SEI+CERT+Oracle+Coding+Standard+for+Java
