# API Gateway Mapping Template / Proxy Passthrough Injection

**MUST NOT** interpolate raw request data into VTL mapping templates or constructed upstream payloads without escaping and schema validation; treat `$input` and `$context` fields as attacker-controlled strings.

**Why:** Naive `$input.json()` splicing into JSON or header templates lets a crafted body break out of the intended structure — forging identity headers, smuggling backend directives, or corrupting the upstream request that the backend trusts because it "came from the gateway."

**Detect:** Audit `*.vm`/VTL templates for direct `$input.json('...')` or `$context.identity.*` writes into headers and bodies without `escapeJson`/`escapeJava`; look for passthrough mode `WHEN_NO_TEMPLATE` on sensitive integrations, and templates that set `X-User-Id` from the body instead of the verified authorizer context.

**Bad:**
```vtl
{ "user": $input.json('$.user'), "role": $input.json('$.role') }
```

**Good:**
```vtl
#set ($user = $input.json('$.user'))
{ "user": "$util.escapeJson($user)",
  "role": "$context.authorizer.claims.role" }
```

**References:** CWE-74, AWS API Gateway mapping template docs, OWASP Injection cheatsheet
