# gRPC

**SHOULD** terminate gRPC behind a proxy that enforces TLS, message-size limits, and method-level authz rather than trusting plaintext backends.

**Why:** gRPC over h2c without interception skips WAF and auth layers, exposing every RPC method to anyone who can reach the port.

**Detect:** `grpc.InsecureServerCreds`, absent `max_receive_message_size`, Envoy routes without `grpc_auth` filters.

**References:** CWE-319, OWASP API 2023, gRPC security best practices

---

**Part of:** [api-design](../categories/api-design.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
