# correctness-pitfalls — full checklist (23 items)

Language-agnostic code-level failure modes.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/correctness-pitfalls.md](../categories/correctness-pitfalls.md) · Index: [SKILL.md](../SKILL.md)

# Big O Notation

**SHOULD** know the complexity of hot paths against realistic input sizes before shipping, not just correctness.

**Why:** An unnoticed linear or worse scan inside a request turns moderate traffic into timeouts and CPU saturation.

**Detect:** `in` membership on lists in loops, sort-then-scan per request, nested loops over collections, no complexity note on hot functions.

**References:** CWE-407, CWE-834, OWASP ASVS V11.1.3/V11.1.4

# Business Logic Workflow Bypass & Abuse

**MUST** enforce step ordering, state transitions, and per-user limits server-side rather than trusting the client's flow.

**Why:** Attackers replay, skip, or race steps to get coupons twice, skip payment, or reach states the design never intended.

**Detect:** State transitions driven by client fields, no server-side state machine, idempotency key absent on money actions, missing per-user rate/limit checks.

**References:** CWE-841, CWE-362, OWASP Business Logic Errors, ASVS 4.x

# Character Encoding

**SHOULD** declare and enforce UTF-8 end to end — files, databases, HTTP headers, and mail — rather than relying on defaults.

**Why:** Mismatched encodings mangle data, and permissive fallback decoding enables parser differentials and XSS via alternate charsets.

**Detect:** Missing `charset=utf-8` in `Content-Type`, `latin-1`/`cp1252` defaults, DB collation not `utf8mb4`, `open()` without `encoding=`.

**References:** CWE-172, CWE-836, OWASP XSS Cheat Sheet, RFC 3629

# Config-Example Template Drift

**SHOULD** keep a committed example config (`config.example.*`) listing every key the code reads, with the real config untracked — and verify in review that the example hasn't drifted from actual required keys.

**Why:** A stale example config is a trap: new deployers hit mysterious failures or silently miss security-relevant settings (TLS flags, auth toggles) that were added to code but never to the template.

**Detect:** diff example-config keys vs keys the code actually reads (grep config-access calls); flag example files missing entirely or missing recently-added settings; CI template-vs-code key comparison where tooling exists.

**References:** twelve-factor config separation, analysis-code config-template practice

# Daylight Saving Time

**SHOULD NOT** compute elapsed time or cron schedules by naive clock arithmetic across DST transitions; **SHOULD** test scheduled jobs and time logic across the spring-forward gap and fall-back overlap in the deployment timezone.

**Why:** Skipped and repeated local hours make jobs fire twice, never fire, or report impossible durations — a bug that hides for months and surfaces exactly at the transition.

**Detect:** Cron with fixed local hours, `timedelta(hours=1)` loops over calendar days, `TZ=America/` with `naive` datetimes, no test freezing the clock at a DST boundary (spring-forward gap, fall-back overlap) in the deployment timezone, scheduler docs silent on which timezone governs.

**References:** NIST SP 800-53 AU-8, IANA tzdb, crontab(5) NOTES on DST

# Dead Code

**SHOULD NOT** ship code paths that cannot be reached (no call site, permanently-off feature flag, disabled branch); a reachable branch that no test exercises is a coverage finding, not dead code.

**Why:** Unreachable branches hide vulnerabilities that no test covers, rot silently, and mislead reviewers into trusting unverified logic.

**Detect:** Functions with zero call sites, `if False`, commented-out blocks, feature flags permanently off.

**References:** CWE-561

# Debouncing

**SHOULD** debounce or throttle high-frequency triggers (keystrokes, resize, webhooks) so bursts do not fan out into redundant work.

**Why:** Without it, each event fires a request or job, overwhelming backends and amplifying a small client into a self-inflicted DoS.

**Detect:** Keyup/scroll/resize handlers calling APIs directly, webhook consumer with no dedupe window, missing `debounce`/`throttle`/rate-limit middleware.

**References:** CWE-770, CWE-400, OWASP API4:2023

# Edge Cases

**SHOULD** test empty, single-element, maximum, zero, negative, and null inputs explicitly rather than trusting the happy path.

**Why:** Unhandled boundary values are where crashes, silent data loss, and auth bypasses surface in production.

**Detect:** Missing tests for `[]`, `0`, `-1`, `None`/`null`, `""`; `if len(x)` guards without else branch; untested max page size.

**References:** CWE-754, CWE-1284, OWASP ASVS 5.1

# Blocking the Shared Concurrency Primitive

**MUST NOT** run CPU-heavy or synchronous blocking calls inside a shared event loop / cooperative-scheduling context.

**Why:** One blocking call stalls every concurrent request on that loop or worker pool, turning a slow endpoint into a full service outage.

**Detect:** sleep/sync file/DB/HTTP calls inside async handlers (e.g. `time.sleep` in `async def`, sync HTTP client calls in handlers), missing offload mechanisms (`run_in_executor`, `spawn_blocking`, dedicated worker pool) for blocking work.

**References:** CWE-400, CWE-662, OWASP ASVS V11.1.3/V11.1.4

# Floating Point Math

**SHOULD NOT** compare binary floating-point values for exact equality or accumulate them over many operations.

**Why:** Rounding error makes `0.1 + 0.2 == 0.3` false and compounds into wrong totals, broken idempotency, and flaky tests.

**Detect:** `== 0.1`, `assert x == y` on floats, `sum(floats)`, `float(` in money/rate code, missing `math.isclose`/`abs(a-b) < eps`.

**References:** CWE-1339, CWE-682, IEEE 754

# Integer Overflow

**MUST NOT** perform arithmetic on externally influenced integers without width or range checks.

**Why:** Wraparound turns a large quantity or price into a negative or tiny value, enabling balance manipulation and buffer misallocation.

**Detect:** `int32`/`uint` on user-supplied counts, `*`/`+` on request fields with no bounds, `parseInt` into fixed-width types, missing `checked_add`/`Math.addExact`.

**References:** CWE-190, CWE-682, CERT INT32-C

# Memory Safety: Buffer Overflow & Use-After-Free

**MUST** bound every buffer write and never dereference freed or dangling memory in unsafe languages.

**Why:** Overflows and use-after-free are classic primitives for arbitrary code execution and privilege escalation.

**Detect:** `strcpy`/`sprintf`/`memcpy` without size checks, raw `malloc`/`free` lifetimes, indexing past array length, missing bounds sanitizer.

**References:** CWE-120, CWE-416, CWE-787, CERT MEM rules

# Merge Conflicts

**MUST NOT** commit unresolved conflict markers or blindly pick one side when merging security-sensitive code.

**Why:** A stray `<<<<<<<` breaks the build, and a wrong-side resolution can silently drop an auth check or re-enable a patched flaw.

**Detect:** `<<<<<<<`, `=======`, `>>>>>>>` in tracked files, conflict resolved without re-running tests, security files merged without review.

**References:** OWASP ASVS 15.2, Git conflict docs

# Off-by-One Errors

**MUST NOT** mix inclusive and exclusive bounds in loops, slices, pagination, and buffer sizes without a stated convention.

**Why:** A single misplaced `<` versus `<=` drops or duplicates records and can read one element past a buffer's end.

**Detect:** `range(len(x)-1)`, `i <= len(`, `arr[n]` where `n == len(arr)`, `LIMIT`/`OFFSET` arithmetic, `pageSize * page` mismatches.

**References:** CWE-193, CWE-119

# Quadratic Complexity & Nested Loops (O(n²) on unbounded input)

**MUST NOT** nest loops over two externally sized collections without a bound on either dimension.

**Why:** A modest payload (10k × 10k) becomes 100M operations, letting one cheap request saturate CPU for everyone.

**Detect:** `for ... for` over request arrays, `.map` inside `.filter` on user lists, join without index, no max-length on both sides.

**References:** CWE-407, CWE-834, OWASP API DoS guidance

# Schema Validation

**MUST** validate every inbound payload against an explicit schema (types, required fields, bounds) before any business logic runs.

**Why:** Unvalidated fields let attackers inject unexpected shapes, extra keys, or oversized values that downstream code mishandles.

**Detect:** Handler reads `request.json[...]` with no validator, missing Pydantic/Zod/JSON Schema, `additionalProperties: true`, mass-assignment from raw body.

**References:** CWE-915, CWE-1289, OWASP ASVS V5.1.3/V5.1.4, OWASP API1:2023

# Storing Money as Floats

**MUST** represent currency as integers in minor units or an exact decimal type, never as binary floating point.

**Why:** Float rounding silently mis-charges customers, breaks reconciliation, and fails audit for financial records.

**Detect:** `float`/`double` in amount, price, balance, total columns or fields; `REAL`/`FLOAT` in migrations; `round(x*100)` casts.

**References:** CWE-1339, CWE-682, PCI DSS 6.5

# Structured Exception Handling (typed errors, no swallowed exceptions, error boundaries)

**MUST** raise typed errors and catch them narrowly at boundaries that can recover, propagating everything else with context instead of letting it vanish or continuing as if nothing failed.

**Why:** Untyped, swallowed exceptions erase the failure signal, so callers proceed on corrupt state, generic handlers leak stack traces to users, and bugs become undiagnosable.

**Detect:** Bare `except:`/`catch(Exception)`, `except Exception: pass`, `catch {}`, `catch (e) {}`, `.catch(() => {})`, ignored `err != nil`, error logged but flow continues, no custom error classes, missing React error boundary at UI roots.

**References:** CWE-390, CWE-209, CWE-703, OWASP ASVS 7.4

# Technical Debt

**MAY** accumulate shortcuts deliberately, but each one must be tracked with an owner and a repayment plan.

**Why:** Untracked debt compounds: security fixes get harder, onboarding slows, and known weak spots quietly become permanent attack surface.

**Detect:** `TODO`/`FIXME`/`HACK` with no ticket, duplicated blocks, dead feature flags, `XXX` markers, no debt entry in the backlog.

**References:** ISO 25010 maintainability, NIST SP 800-160

# Thread Safety

**MUST** protect shared mutable state with locks, atomics, or immutability; never assume single-threaded execution.

**Why:** Unprotected races corrupt data intermittently and produce security holes that only appear under production load.

**Detect:** Shared dict/list mutated without `Lock`/`mutex`/`synchronized`, check-then-act on globals, non-atomic `count += 1`, cached mutable singletons.

**References:** CWE-362, CWE-366, OWASP ASVS V11.1.6

# Time Zones

**MUST** store and compare timestamps in UTC, converting to local time only at the display layer.

**Why:** Mixing local and UTC times corrupts ordering, scheduling, and audit trails when users or servers span zones.

**Detect:** `datetime.now()` / `new Date()` without `tz=utc`, `localtime` in Postgres columns, `TIMESTAMP` instead of `TIMESTAMPTZ`, hardcoded `+08:00` offsets.

**References:** NIST SP 800-53 AU-3, ISO 8601

# Unhandled Async Errors

**MUST** attach an error handler to every async operation (promise/task/future/callback), or register a global unhandled-error hook that fails loudly.

**Why:** An unhandled async error can silently kill a worker, drop a transaction mid-flight, or vanish with no trace — the async analogue of a swallowed exception, and far easier to introduce.

**Detect:** `.then(` without `.catch(`, `await` outside try/catch at entry points, tasks spawned without error propagation, missing global hooks (e.g. `process.on('unhandledRejection')`), floating async calls with no awaited/voided result.

**References:** CWE-391, CWE-248, Node.js unhandledRejection docs, structured-concurrency practices

# Unicode

**MUST NOT** assume one character equals one byte or one code point when measuring, truncating, or comparing user text.

**Why:** Combining marks, surrogate pairs, and normalization variants break length checks, allow look-alike spoofing, and corrupt truncation.

**Detect:** `len(s)` as display width, `substr`/`slice` on user text, missing NFC/NFKC normalization, homoglyph or confusable comparisons absent.

**References:** CWE-176, Unicode TR36, OWASP ASVS 5.2

