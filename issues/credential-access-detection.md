# Credential Access Detection (keylogging, token theft, credential dumping patterns)

**SHOULD** detect credential-harvesting behavior: LSASS/mimikatz dumps, keylogging hooks, OAuth token replay, cloud credential scraping from instance metadata.

**Why:** Stolen credentials are the leading initial-access vector; catching the theft step stops breaches that identity-based controls alone miss.

**Detect:** grep detection content for `T1003`, `lsass`, `mimikatz`, `secretsdump`, `169.254.169.254` access alerts, `GetTokenAlot`/token-replay rules in SIEM configs.

**References:** MITRE ATT&CK TA0006/T1003, NIST SP 800-63B, CWE-522, AWS GuardDuty credential-access detections
