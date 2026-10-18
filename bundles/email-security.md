# email-security — full checklist (4 items)

Mail authentication, brand protection, and email-content trust.

> Generated artifact. Canonical source: `issues/<slug>.md`.

# BIMI & VMC Certificates

**SHOULD** publish BIMI records with a Verified Mark Certificate (VMC) and aligned DMARC policy to authenticate brand-mark display in inboxes.

**Why:** Without BIMI/VMC, spoofed phishing emails render indistinguishable from legitimate brand mail; with it, forged senders visibly fail.

**Detect:** `dig default._bimi.<domain>` for BIMI record; verify logo is SVGZ with valid VMC/CMC; confirm DMARC alignment is a prerequisite (BIMI requires enforcement policy).

**References:** bimigroup.org, Google Postmaster BIMI requirements, M3AAWG sender best practices

# MTA-STS & TLS Reporting

**SHOULD** publish MTA-STS policy (or DANE) requiring TLS for inbound mail, with TLS-RPT monitoring for downgrade attempts.

**Why:** Without MTA-STS, mail can be downgraded to plaintext or redirected via MX hijack silently; TLS-RPT surfaces the interception attempts you'd otherwise never see.

**Detect:** `dig _mta-sts.<domain> TXT` and `https://mta-sts.<domain>/.well-known/mta-sts.txt` for policy (mode=enforce); check `_smtp._tls.<domain>` TLS-RPT record exists.

**References:** RFC 8461 MTA-STS, RFC 8472 TLS-RPT, Google Postmaster Tools

# Lookalike-Domain Monitoring

**SHOULD** continuously monitor for typosquat/lookalike registrations of your brand domains and take takedown action.

**Why:** Brand-adjacent domains (`yourcompany-secure.com`, homoglyph variants) are pre-staged for phishing before you know they exist; takedown is far cheaper before a campaign runs.

**Detect:** review for a monitoring service/cron (Dmarcian, Red Points, custom diff of newly-registered domains vs brand patterns); check homoglyph/keyboard-adjacent variants are in scope.

**References:** M3AAWG brand abuse guidance, Unicode homoglyph attacks, phishing pretexting reports

# Email-Template Injection

**MUST** treat user-controlled data interpolated into transactional emails as untrusted: escape HTML, strip/sanitize URLs, and never render user input as links or markup.

**Why:** Usernames or fields containing `<a href="https://phish...">` turn your trusted, DKIM-signed transactional email into a phishing vector your own domain vouches for.

**Detect:** grep mail templates for raw interpolation of user fields (`{{name}}` without escape, `|safe`, `dangerouslySetInnerHTML`); check URL fields are validated against allow-lists before rendering as links.

**References:** CWE-94 code injection in mail templates, OWASP XSS in email clients guidance

