---
categories: [cloud-network, compliance-privacy]
domains: [governance, infrastructure]
---

# Serverless Execution Environment Reuse Leaking Data Across Invocations

**MUST NOT** cache per-request data — customer records, tokens, decrypted keys — in module-level or global mutable state of a serverless function, because warm containers are shared by later, possibly different, invocations.

**Why:** Lambda and friends reuse a warmed container across tenants' requests when concurrency allows; a global populated during request A can be read during request B, producing cross-customer data disclosure that only appears under load.

**Detect:** In Lambda/Cloud Function/Cloud Run code, flag module-scope dicts, lists, or connection objects that store request-derived values (`current_user = None` at top level then assigned inside the handler), memoized decryption caches keyed loosely, and background threads outliving the handler. Contrast with connection pools (acceptable) versus data caches (not).

**Bad:**
```python
cached_profile = None          # module scope, survives invocations
def handler(event, ctx):
    global cached_profile
    cached_profile = fetch_profile(event["user_id"])
    return {"sso": cached_profile["email"]}
```

**Good:**
```python
def handler(event, ctx):
    profile = fetch_profile(event["user_id"])   # request-local only
    return {"sso": profile["email"]}
```

**References:** CWE-459, AWS Lambda execution environment reuse docs, OWASP Serverless Top 10 (A02)
