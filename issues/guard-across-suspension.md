---
categories: [correctness-pitfalls]
domains: [backend]
---

# Guards Across Suspension Points

**MUST NOT** hold a mutex or guard across a suspension point such as an await, yield, or callback that may take the same lock.

**Why:** A guard that outlives its critical section across a suspension point deadlocks the task or panics a non-reentrant lock at runtime.

**Detect:** grep for await or yield statements inside a lock scope; clippy await_holding_lock catches the Rust case

**References:** rust-clippy, https://github.com/rust-lang/rust-clippy
