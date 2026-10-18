# Certificate-Issuance Monitoring

**SHOULD** alert on any certificate issued for your domains (CT-log monitoring via Certstream/CRT.sh) to detect unauthorized issuance fast.

**Why:** Rogue/mistaken certs for your domain appear in Certificate Transparency logs publicly — if you're not watching, you learn about the fake cert from an outage or a breach report.

**Detect:** check for CT-monitoring service/cron (Censys monitor, Certstream consumer, crt.sh search alerts) covering all brand domains and wildcard patterns; verify alert routing to a responder.

**References:** Certificate Transparency project (certificate-transparency.org), Censys/Certstream monitoring, Google CT policy
