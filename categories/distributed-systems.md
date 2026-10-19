# distributed-systems

Consistency, consensus, coordination across nodes.

## What this category covers

This category covers what changes when state and work are spread across more than one node: agreement, coordination, and the ordering of events where no single clock or process is authoritative. Its member items span consistency models (strong and eventual, CAP tradeoffs), consensus and commitment (Raft, two-phase commit, quorums), coordination primitives (leader election, distributed locks, split-brain fencing, clock skew), and distributed data patterns (change data capture, event sourcing, CQRS, the outbox pattern, consistent hashing, Bloom filters). A reviewer here should ask, for every cross-node decision, which node is authoritative, what happens during a partition, and how a stale participant is prevented from acting. Findings are usually an agreement mechanism that works in the happy path but has no fence, quorum, or idempotency requirement to survive a partition or a delayed leader.

- Consistency models and CAP tradeoffs documented per datastore.
- Consensus and commit protocols: Raft, two-phase commit, read/write quorums.
- Coordination and fencing: leader election, distributed locks, split brain, clock skew.
- Distributed data patterns: change data capture, event sourcing, CQRS, outbox.
- Partitioning and routing: consistent hashing, Bloom filters.

## What it does not cover

- [database](../categories/database.md) — schema, queries, and single-store transaction behavior belong there; how those stores agree across nodes belongs here.
- [messaging-async](../categories/messaging-async.md) — broker configuration, delivery semantics, and consumer handling belong there; the coordination guarantees a distributed workflow depends on belong here.
- [resilience](../categories/resilience.md) — retries, timeouts, circuit breakers, and degradation under dependency failure belong there; correctness of agreement under partition belongs here.
- [scaling-capacity](../categories/scaling-capacity.md) — capacity limits and scaling behavior belong there; distributing keys evenly across nodes in the first place belongs here.

## What a finding here looks like

- a leader that can still serve writes after a new leader was elected, with no epoch fence.
- a distributed lock with no fencing token, so a paused holder's stale write lands after a new holder's.
- ordering decisions resting on wall-clock timestamps across nodes with unbounded clock skew.
- an outbox event published before the transaction that writes the domain change commits.
- a read of inventory or balance satisfied by an eventually consistent replica.
