# Test Determinism & Isolation

**MUST** make tests deterministic: fixed seeds for randomized tests, no shared mutable state between tests, order-independent execution.

**Why:** Nondeterministic tests silently under-verify — a security assertion that passes only in certain orders or seeds gives false confidence, and intermittent failures train teams to re-run rather than investigate.

**Detect:** check for seeded randomness in test fixtures (seed recorded/pinned), test-order randomization enabled with passing results, shared globals/singletons mutated across test files.

**References:** test-isolation practice, flaky-test prevention guidance, property-based testing seed discipline
