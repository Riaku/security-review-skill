# Backward Compatibility

**MUST NOT** remove or rename fields, endpoints, or enum values in a live API without a deprecation window and consumer migration path.

**Why:** Old clients in the wild — mobile apps, webhooks, cached integrations — break instantly on removal, and you cannot force their upgrade.

**Detect:** git diffs deleting response fields/routes without `@deprecated` markers; breaking-change linter (optic, oasdiff) absent from CI.

**References:** OWASP API 2023, Google AIP-180, oasdiff breaking-change rules
