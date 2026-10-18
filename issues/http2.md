---
categories: [api-design]
domains: [backend]
---

# HTTP/2

**SHOULD** enable HTTP/2 only with tuned flow-control windows and stream concurrency limits at the edge.

**Why:** Untuned multiplexing amplifies small-request floods into stream-exhaustion and slow-client window stalls across many logical streams.

**Detect:** `http2_max_concurrent_streams`, `initial_stream_window_size`, absent h2 settings in Envoy/nginx `http2` blocks.

**References:** RFC 9113 §6.9, CWE-400, nginx http2 directives

---

**Part of:** [api-design](../categories/api-design.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
