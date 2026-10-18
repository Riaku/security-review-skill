# HSTS

**SHOULD** Every HTTPS response carry a `Strict-Transport-Security` header with a max-age of at least one year, plus `includeSubDomains` on apex domains.

**Why:** Without HSTS, a single HTTP request or an SSL-stripping proxy can downgrade a connection; the header pins browsers to TLS so later visits can't be intercepted in plaintext.

**Detect:** Grep server and framework configs for `Strict-Transport-Security` and verify `max-age=31536000` or higher. Watch for nginx `add_header` directives in nested locations silently overriding each other.

**Bad:**
```nginx
server {
    listen 443 ssl;
    # no HSTS header at all
    location / { proxy_pass http://app; }
}
```

**Good:**
```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
```

**References:** RFC 6797, CWE-319, OWASP A02:2021 Cryptographic Failures, WSTG-CONF-07