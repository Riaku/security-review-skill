---
categories: [deployment-release, third-party-integrations]
domains: [backend, infrastructure]
---

# 12-Factor Apps

**SHOULD** externalize config to the environment — reaching every backing service (database, queue, cache, SMTP) through an environment-supplied location and credential so the provider or instance can be swapped without a code change — and treat processes as stateless, so no secret or session state is baked into images or local disk.

**Why:** Config compiled into images leaks through registry access and forces rebuilds to rotate credentials, slowing response to a compromise; hardcoded provider hostnames and instance identifiers likewise block credential rotation and moving to a managed or failover instance, and leak internal topology into the repo.

**Detect:** grep images/repos for hardcoded hosts, ports, credentials, connection strings, provider URLs, and instance IDs instead of `env`/`ConfigMap` or injected bindings; check for session data written to container filesystem paths; verify a staging deploy can point at a different provider instance with config only.

**References:** 12factor.net config/stateless factors, 12factor.net/backing-services, OWASP Docker Top 10 D06 (Protect Secrets), CWE-798 hardcoded credentials
