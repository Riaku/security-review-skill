---
categories: [email-security]
domains: [governance]
---

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
