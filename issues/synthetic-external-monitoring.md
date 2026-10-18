# Synthetic External Monitoring

**SHOULD** run synthetic probes from outside the network perimeter to catch outages, TLS problems, and defacement invisible to internal monitoring.

**Why:** Internal checks pass while the public-facing service is down or serving tampered content — the exact failure mode customers experience first.

**Detect:** grep for synthetic checkers (Pingdom, Grafana Synthetic Monitoring, CloudWatch Synthetics) hitting public URLs with content/TLS assertions, not just TCP pings.

**References:** Google SRE Book Ch.6, OWASP Testing Guide 4.0, CWE-295
