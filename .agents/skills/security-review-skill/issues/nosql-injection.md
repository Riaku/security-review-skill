---
categories: [web-api-security]
domains: [backend, data]
---

# NoSQL Query Injection

**MUST NOT** build queries by merging raw user input into query objects; validate types and use explicit field-level operators instead of user-controlled dicts or `$where` clauses.

**Why:** MongoDB-style engines interpret operator keys inside user JSON: `{"pass": {"$ne": ""}}` submitted into a naive `find(body)` authenticates without a password. `$where` with string concatenation goes further, executing arbitrary JavaScript server-side.

**Detect:** Grep for `find(req.body)`, `$where`, `mapReduce` with interpolation, and PyMongo/Mongoose filters whose dict originates from request payloads. Check for missing schema validation (Mongoose strict mode, JSON Schema) on inbound documents.

**Bad:**
```javascript
db.users.find({
  user: req.body.user,
  pass: req.body.pass   // {"$ne":""} bypasses auth
});
```

**Good:**
```javascript
const u = String(req.body.user), p = String(req.body.pass);
db.users.findOne({ user: u, pass: await verify(p) });
```

**References:** CWE-943 NoSQL injection, OWASP NoSQL Injection Prevention Cheat Sheet, MongoDB $where security notes
