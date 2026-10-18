# 12-Factor Apps

**SHOULD** externalize config to the environment and treat processes as stateless, so no secret or session state is baked into images or local disk.

**Why:** Config compiled into images leaks through registry access and forces rebuilds to rotate credentials, slowing response to a compromise.

**Detect:** grep images/repos for hardcoded hosts, ports, and credentials instead of `env`/`ConfigMap`; check for session data written to container filesystem paths.

**References:** 12factor.net config/stateless factors, OWASP Docker Top 10 (D-04 secrets), CWE-798 hardcoded credentials
