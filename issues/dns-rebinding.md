# DNS Rebinding Against Internal Services

**SHOULD** validate `Host`/`Origin` headers and pin DNS resolution at connect time, so a fetch cannot be re-pointed from a public name to a private IP between lookups.

**Why:** A short-TTL record that flips from the attacker's server to `127.0.0.1` smuggles client requests past filters that only checked the name once — a classic route to admin panels and metadata services.

**Detect:** Handlers trusting `Host` for routing; SSRF allowlists validating DNS once instead of at connect; missing `Origin` checks on state-changing endpoints reachable from browsers. Test with a rebinding service like `rbndr.us`.

**Bad:**
```python
if urlparse(url).hostname.endswith(".example.com"):
    fetch(url)   # second lookup may now return 127.0.0.1
```

**Good:**
```python
ip = ipaddress.ip_address(socket.gethostbyname(host))
if not (ip.is_private or ip.is_loopback or ip.is_link_local):
    fetch(pinned_ip_url)   # connect vetted IP, keep SNI/Host pinned
```

**References:** CWE-350, OWASP SSRF Prevention Cheat Sheet, OWASP A10:2021
