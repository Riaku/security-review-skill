# Threat Hunting Practice

**SHOULD** run scheduled, hypothesis-driven hunts over retained telemetry instead of waiting for alerts to fire.

**Why:** Sophisticated intruders operate below alert thresholds for weeks; only proactive searching surfaces the anomalies no rule was written for.

**Detect:** verify a documented hunt cadence, saved hunt queries (KQL/SPL/Lucene) in the SIEM, and hunt findings tracked; flag SIEM used only for alert triage.

**References:** MITRE ATT&CK D3FEND hunt guidance, NIST SP 800-150, SANS threat hunting process
