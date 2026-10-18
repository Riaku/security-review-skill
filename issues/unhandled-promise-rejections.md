# Unhandled Async Errors

**MUST** attach an error handler to every async operation (promise/task/future/callback), or register a global unhandled-error hook that fails loudly.

**Why:** An unhandled async error can silently kill a worker, drop a transaction mid-flight, or vanish with no trace — the async analogue of a swallowed exception, and far easier to introduce.

**Detect:** `.then(` without `.catch(`, `await` outside try/catch at entry points, tasks spawned without error propagation, missing global hooks (e.g. `process.on('unhandledRejection')`), floating async calls with no awaited/voided result.

**References:** CWE-584, CWE-248, Node.js unhandledRejection docs, structured-concurrency practices

---

**Part of:** [correctness-pitfalls](../categories/correctness-pitfalls.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
