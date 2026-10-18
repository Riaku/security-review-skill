# API Key Rotation

**SHOULD** rotate API keys on a defined schedule (90 days typical) and immediately on suspected exposure, with automated rotation rather than manual procedures.

**Why:** Static keys that leak remain usable indefinitely; rotation bounds the window an attacker can exploit stolen credentials.

**Detect:** IAM policies lacking `MaxAge`/rotation alarms, hardcoded keys with no expiry, providers without rotation hooks in CI.

**References:** OWASP ASVS V2.10.4, NIST SP 800-57 part 1 §5.2, CWE-321
