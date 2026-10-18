# Error Tracking

**SHOULD** route unhandled exceptions to an error tracker (Sentry-style) with release, environment, and correlation context — while scrubbing sensitive fields before transmission.

**Why:** Silent failures hide exploitation attempts; conversely, unscrubbed error payloads ship credentials and PII to third-party trackers.

**Detect:** grep for `before_send` / `before_send` scrubbers, `Sentry.init`, and check that breadcrumbs exclude password, authorization, cookie headers.

**References:** OWASP Logging Cheat Sheet, CWE-532, Sentry security docs, Sentry `before_send` filtering
