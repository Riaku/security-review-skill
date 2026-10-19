---
categories: [testing-strategy]
domains: [backend]
---

# Concurrency Stress Testing

**SHOULD** exercise concurrent code with interleaving and stress tests that reproduce races, not only sequential unit tests.

**Why:** Races do not reproduce on the happy path; they reproduce under real interleaving, usually first in production.

**Detect:** a stress target that fires the same handler or critical section from many goroutines/threads with randomized scheduling and repeats, wired into CI; a bare `go test -race` run belongs to sanitizers-in-ci.

**References:** Software Engineering at Google, ch. 20, https://abseil.io/resources/swe-book/html/ch20.html
