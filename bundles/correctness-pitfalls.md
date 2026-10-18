# correctness-pitfalls — full checklist (35 items)

Language-agnostic code-level failure modes.

> Generated artifact. Canonical source: `issues/<slug>.md`.

# Error Handling

**MUST** catch errors at the boundary that can recover, and propagate everything else with context instead of letting it vanish.

**Why:** Swallowed or generic error paths hide failures, leak stack traces to users, and let corrupted state persist silently.

**Detect:** `except:`, `except Exception: pass`, `catch {}`, `catch (e) {}`, `.catch(() => {})`, `err != nil` ignored, `|| pass`

**References:** CWE-390, CWE-209, OWASP ASVS 7.4

# Edge Cases

**SHOULD** test empty, single-element, maximum, zero, negative, and null inputs explicitly rather than trusting the happy path.

**Why:** Unhandled boundary values are where crashes, silent data loss, and auth bypasses surface in production.

**Detect:** Missing tests for `[]`, `0`, `-1`, `None`/`null`, `""`; `if len(x)` guards without else branch; untested max page size.

**References:** CWE-754, CWE-1284, OWASP ASVS 5.1

# Off-by-One Errors

**MUST NOT** mix inclusive and exclusive bounds in loops, slices, pagination, and buffer sizes without a stated convention.

**Why:** A single misplaced `<` versus `<=` drops or duplicates records and can read one element past a buffer's end.

**Detect:** `range(len(x)-1)`, `i <= len(`, `arr[n]` where `n == len(arr)`, `LIMIT`/`OFFSET` arithmetic, `pageSize * page` mismatches.

**References:** CWE-193, CWE-119, MISRA-Loop

# Floating Point Math

**SHOULD NOT** compare binary floating-point values for exact equality or accumulate them over many operations.

**Why:** Rounding error makes `0.1 + 0.2 == 0.3` false and compounds into wrong totals, broken idempotency, and flaky tests.

**Detect:** `== 0.1`, `assert x == y` on floats, `sum(floats)`, `float(` in money/rate code, missing `math.isclose`/`abs(a-b) < eps`.

**References:** CWE-1339, CWE-682, IEEE 754

# Storing Money as Floats

**MUST** represent currency as integers in minor units or an exact decimal type, never as binary floating point.

**Why:** Float rounding silently mis-charges customers, breaks reconciliation, and fails audit for financial records.

**Detect:** `float`/`double` in amount, price, balance, total columns or fields; `REAL`/`FLOAT` in migrations; `round(x*100)` casts.

**References:** CWE-1240, CWE-682, PCI DSS 6.5

# Time Zones

**MUST** store and compare timestamps in UTC, converting to local time only at the display layer.

**Why:** Mixing local and UTC times corrupts ordering, scheduling, and audit trails when users or servers span zones.

**Detect:** `datetime.now()` / `new Date()` without `tz=utc`, `localtime` in Postgres columns, `TIMESTAMP` instead of `TIMESTAMPTZ`, hardcoded `+08:00` offsets.

**References:** CWE-1091, NIST SP 800-53 AU-3, ISO 8601

# Daylight Saving Time

**SHOULD NOT** compute elapsed time or cron schedules by naive clock arithmetic across DST transitions.

**Why:** Skipped and repeated local hours make jobs fire twice, never fire, or report impossible durations.

**Detect:** Cron with fixed local hours, `timedelta(hours=1)` loops over calendar days, `TZ=America/` with `naive` datetimes, missing DST tests near March/November.

**References:** CWE-1091, NIST SP 800-53 AU-8, IANA tzdb

# Unicode

**MUST NOT** assume one character equals one byte or one code point when measuring, truncating, or comparing user text.

**Why:** Combining marks, surrogate pairs, and normalization variants break length checks, allow look-alike spoofing, and corrupt truncation.

**Detect:** `len(s)` as display width, `substr`/`slice` on user text, missing NFC/NFKC normalization, homoglyph or confusable comparisons absent.

**References:** CWE-176, CWE-645, Unicode TR36, OWASP ASVS 5.2

# Character Encoding

**SHOULD** declare and enforce UTF-8 end to end — files, databases, HTTP headers, and mail — rather than relying on defaults.

**Why:** Mismatched encodings mangle data, and permissive fallback decoding enables parser differentials and XSS via alternate charsets.

**Detect:** Missing `charset=utf-8` in `Content-Type`, `latin-1`/`cp1252` defaults, DB collation not `utf8mb4`, `open()` without `encoding=`.

**References:** CWE-172, CWE-836, OWASP XSS Cheat Sheet, RFC 3629

# Thread Safety

**MUST** protect shared mutable state with locks, atomics, or immutability; never assume single-threaded execution.

**Why:** Unprotected races corrupt data intermittently and produce security holes that only appear under production load.

**Detect:** Shared dict/list mutated without `Lock`/`mutex`/`synchronized`, check-then-act on globals, non-atomic `count += 1`, cached mutable singletons.

**References:** CWE-362, CWE-366, OWASP ASVS 12.3

# Blocking the Shared Concurrency Primitive

**MUST NOT** run CPU-heavy or synchronous blocking calls inside a shared event loop / cooperative-scheduling context.

**Why:** One blocking call stalls every concurrent request on that loop or worker pool, turning a slow endpoint into a full service outage.

**Detect:** sleep/sync file/DB/HTTP calls inside async handlers (e.g. `time.sleep` in `async def`, sync HTTP client calls in handlers), missing offload mechanisms (`run_in_executor`, `spawn_blocking`, dedicated worker pool) for blocking work.

**References:** CWE-400, CWE-662, OWASP ASVS 5.3

# Unhandled Async Errors

**MUST** attach an error handler to every async operation (promise/task/future/callback), or register a global unhandled-error hook that fails loudly.

**Why:** An unhandled async error can silently kill a worker, drop a transaction mid-flight, or vanish with no trace — the async analogue of a swallowed exception, and far easier to introduce.

**Detect:** `.then(` without `.catch(`, `await` outside try/catch at entry points, tasks spawned without error propagation, missing global hooks (e.g. `process.on('unhandledRejection')`), floating async calls with no awaited/voided result.

**References:** CWE-584, CWE-248, Node.js unhandledRejection docs, structured-concurrency practices

# Integer Overflow

**MUST NOT** perform arithmetic on externally influenced integers without width or range checks.

**Why:** Wraparound turns a large quantity or price into a negative or tiny value, enabling balance manipulation and buffer misallocation.

**Detect:** `int32`/`uint` on user-supplied counts, `*`/`+` on request fields with no bounds, `parseInt` into fixed-width types, missing `checked_add`/`Math.addExact`.

**References:** CWE-190, CWE-682, CERT INT32-C

# Schema Validation

**MUST** validate every inbound payload against an explicit schema (types, required fields, bounds) before any business logic runs.

**Why:** Unvalidated fields let attackers inject unexpected shapes, extra keys, or oversized values that downstream code mishandles.

**Detect:** Handler reads `request.json[...]` with no validator, missing Pydantic/Zod/JSON Schema, `additionalProperties: true`, mass-assignment from raw body.

**References:** CWE-915, CWE-1289, OWASP ASVS 5.2, OWASP API1:2023

# Debouncing

**SHOULD** debounce or throttle high-frequency triggers (keystrokes, resize, webhooks) so bursts do not fan out into redundant work.

**Why:** Without it, each event fires a request or job, overwhelming backends and amplifying a small client into a self-inflicted DoS.

**Detect:** Keyup/scroll/resize handlers calling APIs directly, webhook consumer with no dedupe window, missing `debounce`/`throttle`/rate-limit middleware.

**References:** CWE-770, CWE-400, OWASP API4:2023

# Big O Notation

**SHOULD** know the complexity of hot paths against realistic input sizes before shipping, not just correctness.

**Why:** An unnoticed linear or worse scan inside a request turns moderate traffic into timeouts and CPU saturation.

**Detect:** `in` membership on lists in loops, sort-then-scan per request, nested loops over collections, no complexity note on hot functions.

**References:** CWE-407, CWE-834, OWASP ASVS 5.3

# Technical Debt

**MAY** accumulate shortcuts deliberately, but each one must be tracked with an owner and a repayment plan.

**Why:** Untracked debt compounds: security fixes get harder, onboarding slows, and known weak spots quietly become permanent attack surface.

**Detect:** `TODO`/`FIXME`/`HACK` with no ticket, duplicated blocks, dead feature flags, `XXX` markers, no debt entry in the backlog.

**References:** CWE-1152, ISO 25010 maintainability, NIST SP 800-160

# Dead Code

**SHOULD NOT** ship code paths that are never reached or never exercised by tests.

**Why:** Unreachable branches hide vulnerabilities that no test covers, rot silently, and mislead reviewers into trusting unverified logic.

**Detect:** Functions with zero call sites, `if False`, commented-out blocks, feature flags permanently off, coverage reports showing 0 hits.

**References:** CWE-561, CWE-1152, MISRA DEADCODE

# Merge Conflicts

**MUST NOT** commit unresolved conflict markers or blindly pick one side when merging security-sensitive code.

**Why:** A stray `<<<<<<<` breaks the build, and a wrong-side resolution can silently drop an auth check or re-enable a patched flaw.

**Detect:** `<<<<<<<`, `=======`, `>>>>>>>` in tracked files, conflict resolved without re-running tests, security files merged without review.

**References:** CWE-1152, OWASP ASVS 15.2, Git conflict docs

# Quadratic Complexity & Nested Loops (O(n²) on unbounded input)

**MUST NOT** nest loops over two externally sized collections without a bound on either dimension.

**Why:** A modest payload (10k × 10k) becomes 100M operations, letting one cheap request saturate CPU for everyone.

**Detect:** `for ... for` over request arrays, `.map` inside `.filter` on user lists, join without index, no max-length on both sides.

**References:** CWE-407, CWE-834, OWASP API DoS guidance

# Structured Exception Handling (typed errors, no swallowed exceptions, error boundaries)

**MUST** raise typed errors and catch them narrowly at defined boundaries; never blanket-catch and continue as if nothing failed.

**Why:** Untyped, swallowed exceptions erase the failure signal, so callers proceed on corrupt state and bugs become undiagnosable.

**Detect:** Bare `except:`/`catch(Exception)`, error logged but flow continues, no custom error classes, missing React error boundary at UI roots.

**References:** CWE-390, CWE-703, OWASP ASVS 7.4

# OS Command Injection (CWE-78)

**MUST NOT** Pass user input into shell commands; invoke programs with argument arrays, no shell interpolation.

**Why:** `;`, `|`, and backticks turn an argument into arbitrary command execution.

**Detect:** `os.system`, `subprocess` with `shell=True`, `Runtime.exec`, `$()`/backticks in built command strings.

**References:** CWE-78, OWASP A03:2021, OWASP Command Injection guidance

# Regular Expression DoS (ReDoS)

**MUST NOT** run user-supplied or unbounded text against regexes containing nested quantifiers or ambiguous alternation.

**Why:** Catastrophic backtracking turns a short malicious string into exponential CPU time, freezing the request thread or worker.

**Detect:** `(a+)+`, `(a|a)*`, `(.*)*` patterns, `re.match`/`RegExp.test` on raw input, no timeout or RE2/DFA engine configured.

**References:** CWE-1333, CWE-400, OWASP ReDoS, RE2 docs

# Dynamic Code Evaluation of User Input (eval/exec)

**MUST NOT** pass any externally influenced string to `eval`, `exec`, `Function`, or template code execution.

**Why:** Evaluating attacker-controlled text is remote code execution — full host compromise, no sandbox assumed.

**Detect:** `eval(`, `exec(`, `new Function(`, `os.system(`, `subprocess` with `shell=True` on input, Jinja `|safe`/`Template(user_str)`.

**References:** CWE-94, CWE-95, OWASP Injection, OWASP ASVS 5.2

# Memory Safety: Buffer Overflow & Use-After-Free

**MUST** bound every buffer write and never dereference freed or dangling memory in unsafe languages.

**Why:** Overflows and use-after-free are classic primitives for arbitrary code execution and privilege escalation.

**Detect:** `strcpy`/`sprintf`/`memcpy` without size checks, raw `malloc`/`free` lifetimes, indexing past array length, missing bounds sanitizer.

**References:** CWE-120, CWE-416, CWE-787, CERT MEM rules

# Business Logic Workflow Bypass & Abuse

**MUST** enforce step ordering, state transitions, and per-user limits server-side rather than trusting the client's flow.

**Why:** Attackers replay, skip, or race steps to get coupons twice, skip payment, or reach states the design never intended.

**Detect:** State transitions driven by client fields, no server-side state machine, idempotency key absent on money actions, missing per-user rate/limit checks.

**References:** CWE-840, CWE-362, OWASP Business Logic Errors, ASVS 4.x

# Operator Finalizer Leaks Blocking Resource Deletion

**MUST** ensure operators remove their finalizers on owned resources even when reconciliation errors, so deletion never hangs indefinitely.

**Why:** A leaked finalizer leaves resources stuck in Terminating, blocking namespace deletion and cascading cleanup failures across the cluster.

**Detect:** Resources with `metadata.finalizers` referencing an operator whose controller is down; namespace stuck `Terminating` with lingering finalizers.

**References:** K8s docs finalizers, etcd garbage collection, CWE-404, operator-sdk finalizer patterns

# Missing ownerReferences Causing Orphaned Managed Resources

**SHOULD** set `ownerReferences` on every resource a controller creates so cascading deletion reclaims them automatically.

**Why:** Orphaned resources accumulate invisibly, leaking quotas, secrets, and network policies after their parent is gone.

**Detect:** Created resources lacking `metadata.ownerReferences`; garbage collector cannot trace children; orphan count grows over time.

**References:** K8s docs garbage collection, ownerReferences, CWE-404, operator-sdk ownership patterns

# ConfigMap Hot-Reload Assumption for Environment Variables

**MUST NOT** rely on environment-variable-injected ConfigMaps updating at runtime; env vars are fixed at container start, so mount files or restart the pod.

**Why:** Teams assume config changes propagate live, then ship with stale credentials or feature flags after a ConfigMap update.

**Detect:** `envFrom: configMapRef` where the app expects live updates; no checksum annotation or rollout trigger on ConfigMap change.

**References:** K8s docs configmap env immutability, CWE-676, Bitnami/Flux config-reload patterns

# Zombie Process Reaping Handled in Container PID 1

**MUST** ensure the container's PID 1 reaps orphaned child processes, via an init system (tini/dumb-init) or a reaping-aware entrypoint.

**Why:** A non-reaping PID 1 lets zombies accumulate until the PID limit is hit, blocking new process spawns and stalling the container.

**Detect:** Container PID 1 is a shell or app without `--reaping`; `docker top`/`ps` shows defunct `<defunct>` entries; no tini/dumb-init in image.

**References:** CIS Docker 5.x, CWE-459, tini/dumb-init docs, Kubernetes init container patterns

# Durability Acknowledgment Policy

**MUST** acknowledge writes only after they are durably persisted (sync disk and/or quorum replication) for data where loss is unacceptable — payments, orders, credential changes; latency-first acks are permitted only for reversible data (likes, views, logs).

**Why:** Ack-before-persist means a crash between ack and write silently destroys confirmed data; the client believes the operation succeeded and never retries.

**Detect:** review write paths for ack-before-flush/async-persist on critical entities; check DB durability settings (`synchronous_commit`, replication ack level, fsync) against the data's loss tolerance.

**References:** DDIA durability/replication chapters, Postgres synchronous_commit docs, latency-vs-durability trade-off

# Backfill Idempotency at Pipeline Scale

**MUST** make pipeline backfills/re-runs idempotent: reprocessing a date range produces the same result, never duplicates or double-counts.

**Why:** Every data team eventually re-runs a week of jobs; non-idempotent backfills double revenue figures or duplicate records that take months to discover and unwind.

**Detect:** check jobs use MERGE/upsert/overwrite-partition semantics vs append; look for run-id dedupe keys; review backfill runbook for "safe to re-run" statement per job.

**References:** DDIA idempotent consumers, dbt incremental materializations, Airflow clear/backfill semantics

# Ledger Invariant Checks

**MUST** enforce ledger invariants continuously: sum of debits equals sum of credits, no negative balances where prohibited, every money movement has a counter-entry.

**Why:** Silent ledger drift (rounding, partial writes, bugs) compounds into real financial loss; systems without invariant checks discover errors at reconciliation time — too late to cheaply fix.

**Detect:** check for invariant assertions in the ledger layer (double-entry enforcement, balance checks in transactions), scheduled integrity queries, and alarm (not just log) on violation.

**References:** Double-entry bookkeeping in software (Martin Fowler), Stripe financial-modeling talks, PCI-DSS 5/financial integrity practice

# DST-Transition Behavior Test

**SHOULD** test scheduled jobs and time logic across DST transitions (spring-forward gap, fall-back overlap) in the deployment timezone.

**Why:** Cron jobs silently skip or double-fire at DST boundaries; "runs every 2h" becomes 23 or 25 runs twice a year — a bug that hides for months and hits exactly when you're asleep.

**Detect:** check for tests that freeze time at DST boundaries (e.g. 2026-03-08 02:30 US), cron schedules using UTC vs local TZ, and scheduler docs stating which timezone governs; flag local-TZ cron for critical jobs.

**References:** cron DST pitfalls (crontab(5) NOTES), NTP/timezone best practices, ICU timezone docs

# Config-Example Template Drift

**SHOULD** keep a committed example config (`config.example.*`) listing every key the code reads, with the real config untracked — and verify in review that the example hasn't drifted from actual required keys.

**Why:** A stale example config is a trap: new deployers hit mysterious failures or silently miss security-relevant settings (TLS flags, auth toggles) that were added to code but never to the template.

**Detect:** diff example-config keys vs keys the code actually reads (grep config-access calls); flag example files missing entirely or missing recently-added settings; CI template-vs-code key comparison where tooling exists.

**References:** twelve-factor config separation, analysis-code config-template practice

