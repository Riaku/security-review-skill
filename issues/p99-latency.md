# p99 Latency

**SHOULD** track and alert on p99 (not just average) latency for critical endpoints and dependency calls.

**Why:** Averages hide tail latency; slow-response attacks like zip bombs, regex bombs, and resource exhaustion show up first in the p99 tail while means look healthy.

**Detect:** grep dashboards/alerts for `histogram_quantile(0.99` or `p99`; flag services whose SLOs use only mean/median latency.

**References:** Google SRE Workbook SLI chapter, CWE-400, NIST SP 800-207 zero-trust monitoring
