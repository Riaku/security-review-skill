# DNS Propagation

**SHOULD** Lower record TTLs to 300 seconds or less well before a planned cutover, and keep them low until the migration is confirmed stable.

**Why:** Stale caches holding the old IP keep sending users to a decommissioned endpoint; that endpoint may be released, re-IP'd, or claimed by someone else, producing silent traffic loss or a takeover window.

**Detect:** Look for a TTL-lowering step in the change plan ahead of the cutover date. Query `dig +noall +answer SOA <zone>` for current TTLs; flag runbooks that flip records without waiting out the old TTL.

**Bad:**
```bash
# cutover now while old records are cached for 24h
dig A old.app.example.com          # ttl = 86400
```

**Good:**
```bash
# 48h before cutover: TTL 86400 -> 300, wait it out, then flip
dig +short A app.example.com @8.8.8.8   # verify resolvers agree
```

**References:** RFC 2181, AWS Route 53 failover/TTL guidance, Google Cloud DNS caching docs
