---
categories: [scaling-capacity, sre-incidents]
domains: [reliability]
---

# Stateless Services & Sticky-Session Affinity

**SHOULD** keep session and application state external (datastore, token) so any replica can serve any request; **SHOULD NOT** rely on sticky sessions to make a stateful design work — if affinity is required (websockets, streaming), make it explicit, session-aware, and resilient to node loss.

**Why:** Affinity as a patch for server-side state silently breaks horizontal scaling — a rebalanced or failed node drops every "remembered" session, and scale-out multiplies the problem; locally stored sessions break autoscaling and failover the same way, silently logging users out or losing their cart when a node is killed.

**Detect:** grep LB config for `sticky`, `affinity: cookie`, `sessionAffinity: ClientIP`; check whether session state lives in-app vs external store; `session.save_path` on local disk, `JSESSIONID` sticky sessions, writes to `/tmp` or pod-local volumes; test node drain behavior.

**References:** Kubernetes service sessionAffinity docs, AWS ALB stickiness docs, The Twelve-Factor App (processes)
