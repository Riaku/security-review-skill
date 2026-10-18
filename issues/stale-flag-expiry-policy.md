# Stale-Flag Expiry Policy

**SHOULD** give every feature flag an owner and expiry; flags past expiry trigger cleanup tickets, and long-lived flags are treated as config debt.

**Why:** Zombie flags accumulate branches that no one understands, each a latent config-drift and dead-code hazard; flag sprawl measurably degrades codebase health.

**Detect:** grep flag definitions for expiry/owner metadata; count flags older than N months without cleanup; check flag service (LaunchDarkly/Unleash) for stale-flag reports and kill dates.

**References:** Feature-Toggle engineering (Fowler), LaunchDarkly stale-flag governance, Unleash flag lifecycle
