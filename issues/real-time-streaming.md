# Real-time Streaming

**MUST** authorize each stream subscription per-user; never broadcast a channel that any authenticated client can name and join.

**Why:** Predictable stream IDs let one user subscribe to another's private feed, turning a chat or notification channel into a data leak.

**Detect:** `channel.subscribe(channelName)` without per-user ACL check; predictable IDs like `order-{id}` with no ownership verification.

**References:** OWASP API1:2023, CWE-285, Ably/Pusher channel authorization docs
