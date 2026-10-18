# Kill-Switch Verification

**SHOULD** test that emergency feature kill-switches actually work (flip in staging, verify behavior) before relying on them in production.

**Why:** An untested kill-switch is a rumor: the flag path may be dead code, the config may not propagate, or the dependency may be the very thing that's failing.

**Detect:** check for scheduled kill-switch drills with recorded results; verify each critical feature has a flag whose off-path is exercised in tests; confirm flag-service outage behavior is a defined, tested state.

**References:** Netflix chaos/kill-switch practice, feature-flag resilience patterns, circuit-breaker companion issue
