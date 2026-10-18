# Distributed Locks

**MUST** attach a fencing token to every lock grant and have the resource reject operations carrying a stale token, never trusting lock-held-alone.

**Why:** A lock holder paused past its TTL acts after another node acquired the same lock; without fencing, both mutate the resource concurrently.

**Detect:** grep for `redis.lock`/`Redlock` usage without passing a monotonic token to the write path, missing `SET NX PX` expiry, lock release without owner-ID verification.

**References:** Kleppmann "How to do distributed locking", Martin Farber Redlock critique, CWE-662
