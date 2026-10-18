# Lateral Movement Detection (post-compromise horizontal motion in cloud/host)

**SHOULD** alert on post-compromise horizontal motion: unusual SSH/WinRM hops, mass SMB enumeration, anomalous role assumption across accounts.

**Why:** Once inside, attackers pivot toward crown jewels; without motion alerts, breach dwell time stretches to months while one foothold becomes total compromise.

**Detect:** grep detection rules for `lateral_movement`, `T1021`, `remote_services`, `admin_shares`, `PassTheHash`, unusual-login detections in SIEM/YARA-L/Sigma rules.

**References:** MITRE ATT&CK TA0008/T1021, NIST SP 800-61, Sigma lateral-movement rules, AWS GuardDuty UnauthorizedAccess
