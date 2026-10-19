# email-security — full checklist (6 items)

Mail authentication, brand protection, and email-content trust.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/email-security.md](../categories/email-security.md) · Index: [SKILL.md](../SKILL.md)

# BIMI & VMC Certificates

**SHOULD** publish BIMI records with a Verified Mark Certificate (VMC) and aligned DMARC policy to authenticate brand-mark display in inboxes.

**Why:** Without BIMI/VMC, spoofed phishing emails render indistinguishable from legitimate brand mail; with it, forged senders visibly fail.

**Detect:** `dig default._bimi.<domain>` for BIMI record; verify the logo is SVG Portable/Secure (SVG P/S, commonly served as .svgz) with a valid VMC/CMC; confirm DMARC alignment is a prerequisite (BIMI requires enforcement policy).

**References:** bimigroup.org, Google Postmaster BIMI requirements, M3AAWG sender best practices

# Email Bounce Handling

**MUST** consume hard bounces and spam complaints programmatically and feed them into a suppression list so invalid addresses are never mailed again.

**Why:** Mailing dead addresses tanks sender reputation; Gmail and Outlook then divert the whole domain's legitimate mail to spam, and ignored abuse complaints can get the sending IP delisted for weeks.

**Detect:** Check whether SES/SendGrid bounce and complaint notifications have a live SNS consumer — a notification config with no subscriber is the classic gap. Grep for suppression checks before send, and for retry loops that requeue bounced mail.

**Bad:**
```python
for addr in mailing_list:
    send(to=addr, ...)   # bounces go nowhere; we re-send next campaign anyway
```

**Good:**
```python
if suppressed(addr):     # populated from SNS bounce/complaint consumer
    continue
send(to=addr, ...)
```

**References:** AWS SES bounce & complaint handling docs, Gmail Sender Guidelines, M3AAWG sender best practices

# Email-Template Injection

**MUST** treat user-controlled data interpolated into transactional emails as untrusted: escape HTML, strip/sanitize URLs, and never render user input as links or markup.

**Why:** Usernames or fields containing `<a href="https://phish...">` turn your trusted, DKIM-signed transactional email into a phishing vector your own domain vouches for.

**Detect:** grep mail templates for raw interpolation of user fields (`{{name}}` without escape, `|safe`, `dangerouslySetInnerHTML`); check URL fields are validated against allow-lists before rendering as links.

**References:** CWE-94 code injection in mail templates, OWASP XSS in email clients guidance

# Lookalike-Domain Monitoring

**SHOULD** continuously monitor for typosquat/lookalike registrations of your brand domains and take takedown action.

**Why:** Brand-adjacent domains (`yourcompany-secure.com`, homoglyph variants) are pre-staged for phishing before you know they exist; takedown is far cheaper before a campaign runs.

**Detect:** review for a monitoring service/cron (Dmarcian, Red Points, custom diff of newly-registered domains vs brand patterns); check homoglyph/keyboard-adjacent variants are in scope.

**References:** M3AAWG brand abuse guidance, Unicode homoglyph attacks, phishing pretexting reports

# MTA-STS & TLS Reporting

**SHOULD** publish MTA-STS policy (or DANE) requiring TLS for inbound mail, with TLS-RPT monitoring for downgrade attempts.

**Why:** Without MTA-STS, mail can be downgraded to plaintext or redirected via MX hijack silently; TLS-RPT surfaces the interception attempts you'd otherwise never see.

**Detect:** `dig _mta-sts.<domain> TXT` and `https://mta-sts.<domain>/.well-known/mta-sts.txt` for policy (mode=enforce); check `_smtp._tls.<domain>` TLS-RPT record exists.

**References:** RFC 8461 MTA-STS, RFC 8472 TLS-RPT, Google Postmaster Tools

# SPF, DKIM & DMARC

**MUST** publish SPF, DKIM, and a DMARC record ending in a rejecting policy for every domain that sends mail, with alignment verified for each sending service.

**Why:** Without all three, lookalike domains can send convincing spoofed mail from your brand; a record stuck at `p=none` reports the problem but protects nobody against phishing of your customers.

**Detect:** Run `dig TXT <domain>` and `dig TXT _dmarc.<domain>`; flag `p=none` with no `sp` subdomain policy. Enumerate senders (SES, Mailchimp, Zendesk) and confirm each is SPF-included or DKIM-signing. Check for conflicting SPF records.

**Bad:**
```
_dmarc.example.com.  TXT  "v=DMARC1; p=none"        # monitoring only
(no DKIM signing from the marketing platform)
```

**Good:**
```
"v=DMARC1; p=reject; sp=reject; rua=mailto:dmarc@example.com; pct=100"
SPF: "v=spf1 include:amazonses.com -all"
```

**References:** RFC 9989 (DMARC), RFC 6376 (DKIM), RFC 7208 (SPF), CWE-290

