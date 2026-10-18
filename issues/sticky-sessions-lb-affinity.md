# Sticky Sessions & Load-Balancer Affinity

**SHOULD NOT** rely on sticky sessions to make a stateful design work; if affinity is required (websockets, streaming), make it explicit, session-aware, and resilient to node loss.

**Why:** Affinity as a patch for server-side state silently breaks horizontal scaling — a rebalanced or failed node drops every "remembered" session, and scale-out multiplies the problem.

**Detect:** grep LB config for `sticky`, `affinity: cookie`, `sessionAffinity: ClientIP`; check whether session state lives in-app vs external store; test node drain behavior.

**References:** Kubernetes service sessionAffinity docs, AWS ALB stickiness docs, stateless-services issue
