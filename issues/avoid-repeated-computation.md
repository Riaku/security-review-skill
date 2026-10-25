---
categories: [correctness-pitfalls, scaling-capacity]
domains: [backend, reliability]
---

# Repeated Computation on Invariant Inputs

**MUST NOT** recompute inside a loop, or per request, a pure value whose inputs do not change between iterations, and **MUST** bound any memoization of it by size or lifetime.

**Why:** A regex compiled per row, a timezone or config file parsed per request, or an expensive pure function called inside a nested loop multiplies one cheap request into thousands of operations, so CPU scales with input size instead of with work; the cache added to fix it becomes the next memory leak when nothing evicts from it.

**Detect:** calls inside a loop body whose arguments are loop-invariant — `re.compile` in a loop, `json.loads` of a constant, `ZoneInfo`/`DateTimeFormatter` rebuilt per request; pure helpers called with identical arguments in nested loops; `memoize`/`lru_cache`/`sync.Once` use without a max size or key check that covers every input the result depends on.

**References:** CWE-407, CWE-1176
