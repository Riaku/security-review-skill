# email-security

Mail authentication, brand protection, and email-content trust.

## What this category covers

This category covers whether mail sent from your domain is authenticated and whether the content it carries can be abused. Items span sender authentication and alignment, brand display and lookalike-domain monitoring, transport security for inbound mail, list hygiene and sender reputation, and the trust applied to user data rendered into email templates. A reviewer should expect to see DNS records, transactional and bulk mail templates, and the bounce and complaint consumer for the sending provider.

- Sender authentication and alignment — SPF, DKIM, and a DMARC policy that ends in enforcement, aligned for each sending service.
- Brand protection — BIMI with a Verified Mark Certificate, and continuous monitoring for typosquat and homoglyph brand domains.
- Transport security for inbound mail — MTA-STS or DANE policy with TLS reporting to surface downgrade attempts.
- List hygiene and sender reputation — hard bounces and complaints consumed into a suppression list before the next send.
- Email-content trust — escaping and sanitizing user-controlled data interpolated into transactional templates.

## What it does not cover

- [web-api-security](../categories/web-api-security.md) — general injection sinks (SQL, command, template) and webhook consumer trust belong there; rendering user data into a signed email template is scoped here.
- [third-party-integrations](../categories/third-party-integrations.md) — OAuth scope minimization and integration credential sprawl belong there; the sending-provider bounce and complaint pipeline is scoped here.
- [web-client-security](../categories/web-client-security.md) — browser rendering concerns such as CSP and cookie flags belong there; what an email client receives and renders is scoped here.

## What a finding here looks like

- A DMARC record at `p=none` with no subdomain policy, so spoofed mail is monitored but never blocked.
- A sending platform that is neither SPF-included nor DKIM-signing, so its mail fails alignment.
- A bounce or complaint notification configured with no live subscriber, so invalid addresses are mailed again.
- A transactional template interpolating a username or URL field into HTML without escaping, turning signed mail into a phishing vector.
- No monitoring for typo or homoglyph variants of a brand domain before a campaign runs.
