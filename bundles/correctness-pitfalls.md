# correctness-pitfalls — full checklist (41 items)

Language-agnostic code-level failure modes.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/correctness-pitfalls.md](../categories/correctness-pitfalls.md) · Index: [SKILL.md](../SKILL.md)

# Abort on Unexpected Error

**MUST** stop the current operation when an unanticipated exception reaches a generic handler, because application state is unknown.

**Why:** Continuing after an unexpected fault means acting on partially applied state - the path to double-spend, skipped authorization or silent corruption.

**Detect:** `catch (Exception`/`except Exception:`/`catch (Throwable` blocks that log and continue instead of rethrowing or aborting the unit of work.

**References:** SAFECode Fundamental Practices v3 (2018), https://safecode.org/wp-content/uploads/2018/03/SAFECode_Fundamental_Practices_for_Secure_Software_Development_March_2018.pdf

# Bidirectional Control Characters

**MUST** reject bidirectional override and zero-width characters in source, templates, and configuration, failing CI when a file contains them.

**Why:** Direction-override and invisible glyphs let a reviewer see one order of tokens while the compiler or browser executes another.

**Detect:** eslint-plugin-security detect-bidi-characters, or grep -rP '[\x{202A}-\x{202E}\x{2066}-\x{2069}]'

**References:** eslint-plugin-security, https://github.com/eslint-community/eslint-plugin-security, Trojan Source, https://trojansource.codes

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

# Check Return Values

**MUST** check and act on the return value of every call that can fail, including writes, closes, and authorization lookups.

**Why:** An ignored failure leaves the system in a state the next line assumes is valid, so a failed check silently becomes an allow.

**Detect:** grep discarded results: `_ = `, `except.*:\s*pass`, `if err != nil { }` with an empty body, `(void)` casts, and bare `write(`/`close(`/`send(` statements.

**References:** CWE Top 25 (2024), https://cwe.mitre.org/top25/archive/2024/2024_cwe_top25.html, SEI CERT C Coding Standard, https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard

# Config-Example Template Drift

**SHOULD** keep a committed example config (`config.example.*`) listing every key the code reads, with the real config untracked — and verify in review that the example hasn't drifted from actual required keys.

**Why:** A stale example config is a trap: new deployers hit mysterious failures or silently miss security-relevant settings (TLS flags, auth toggles) that were added to code but never to the template.

**Detect:** diff example-config keys vs keys the code actually reads (grep config-access calls); flag example files missing entirely or missing recently-added settings; CI template-vs-code key comparison where tooling exists.

**References:** twelve-factor config separation, analysis-code config-template practice

# Constant Format Strings

**MUST NOT** pass untrusted data as a format string to printf-style, logging, or template formatting functions.

**Why:** A user-controlled format string reads and writes memory through `%n`/`%s`, and the same mistake in loggers corrupts output.

**Detect:** grep `printf(`, `syslog(`, `fprintf(`, `fmt.Fprintf(w, <var>` and `String.format(<var>` where the first argument is not a string literal.

**References:** CWE Top 25, https://cwe.mitre.org/top25/, SEI CERT C Coding Standard (FIO30-C), https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard

# Cross-Boundary Ownership Rule

**MUST** define, for each resource crossing a language or runtime boundary, who allocates it, who frees it, and which side owns it.

**Why:** When both sides assume the other frees, memory leaks; when both free, the second free is a write primitive. Ambiguous ownership across a boundary is a memory-safety bug waiting for load.

**Detect:** judgment: the FFI or native interface declarations and their doc comments — every opaque pointer, buffer, and handle has a stated owner and free path.

**References:** ANSSI Secure Rust Guidelines, https://anssi-fr.github.io/rust-guide/, CWE-415 Double Free

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

# FFI Failure Isolation

**MUST** isolate foreign or abort-capable code at the boundary and convert its failures into the host runtime's error model.

**Why:** An exception or panic crossing a language boundary is undefined behaviour in most runtimes, and an abort takes the whole process with it. Catching at the boundary keeps the failure local and attributable.

**Detect:** grep FFI wrappers for calls into foreign code with no `catch_unwind`/`try`/`except` around them, and for `abort`/`exit` on error paths.

**References:** ANSSI Secure Rust Guidelines, https://anssi-fr.github.io/rust-guide/, CWE-248 Uncaught Exception

# File Descriptor Hygiene

**MUST** open every descriptor that carries secrets or privileged handles close-on-exec, so spawned child processes cannot inherit them.

**Why:** An inherited descriptor is a live handle to a secret in a process that was never granted it, and it survives long after the request that opened it.

**Detect:** grep `open(`, `socket(`, `os.Open`, `FileStream` for missing `O_CLOEXEC`/`FD_CLOEXEC`/close-on-exec, prioritising descriptors for key material, database sockets and log files; flag subprocess spawns that inherit the full descriptor table.

**References:** SEI CERT C Coding Standard, https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard

# Floating Point Math

**SHOULD NOT** compare binary floating-point values for exact equality or accumulate them over many operations.

**Why:** Rounding error makes `0.1 + 0.2 == 0.3` false and compounds into wrong totals, broken idempotency, and flaky tests.

**Detect:** `== 0.1`, `assert x == y` on floats, `sum(floats)`, `float(` in money/rate code, missing `math.isclose`/`abs(a-b) < eps`.

**References:** CWE-1339, CWE-682, IEEE 754

# Guards Across Suspension Points

**MUST NOT** hold a mutex or guard across a suspension point such as an await, yield, or callback that may take the same lock.

**Why:** A guard that outlives its critical section across a suspension point deadlocks the task or panics a non-reentrant lock at runtime.

**Detect:** grep for await or yield statements inside a lock scope; clippy await_holding_lock catches the Rust case

**References:** rust-clippy, https://github.com/rust-lang/rust-clippy

# Initialize Memory Before Use

**MUST** initialize every buffer, struct, and allocation before it is read, and zero padding in structures passed across a trust boundary.

**Why:** An uninitialized read returns whatever the previous owner left there, leaking data and making security decisions nondeterministic.

**Detect:** MemorySanitizer build (`-fsanitize=memory`) in CI, plus grep for `malloc(` followed by field reads with no `memset`/struct initializer.

**References:** SEI CERT C Coding Standard, https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard

# Input Validation

**MUST** Validate all external input against type, length, range, and format allowlists at the trust boundary.
**MUST** validate every inbound payload against an explicit schema (types, required fields, bounds) before any business logic runs.

**Why:** Downstream code assumes validated data; one unchecked field becomes the injection vector, and unvalidated fields let attackers inject unexpected shapes, extra keys, or oversized values that downstream code mishandles.

**Detect:** Handlers reading `request.params`/body straight into logic; missing pydantic/Zod/Joi or `@Valid`; `request.json[...]` read with no validator or JSON Schema, `additionalProperties: true`, mass-assignment from raw body.

**References:** OWASP A03:2021, CWE-20, OWASP Input Validation Cheat Sheet, CWE-915, CWE-1289, OWASP ASVS V5.1.3/V5.1.4, OWASP API1:2023

# Integer Overflow

**MUST NOT** perform arithmetic on externally influenced integers without width or range checks.

**Why:** Wraparound turns a large quantity or price into a negative or tiny value, enabling balance manipulation and buffer misallocation.

**Detect:** `int32`/`uint` on user-supplied counts, `*`/`+` on request fields with no bounds, `parseInt` into fixed-width types, missing `checked_add`/`Math.addExact`.

**References:** CWE-190, CWE-682, CERT INT32-C

# Memory-Safe by Default

**SHOULD** implement parsers and other untrusted-input handling in a memory-safe language or runtime.

**Why:** Memory-safety defects are the largest share of exploitable weakness classes, and they disappear entirely in a memory-safe runtime.

**Detect:** `pygount` language mix for newly added parsers and protocol decoders; a new C/C++ component on an untrusted-input path is the finding (unsafe blocks inside Rust/Go code belong to unsafe-code-confinement).

**References:** CWE Top 25 (2024), https://cwe.mitre.org/top25/archive/2024/2024_cwe_top25.html, The Rustonomicon, https://doc.rust-lang.org/nomicon/, CISA Secure by Design, https://www.cisa.gov/securebydesign

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

# No I/O Under Lock

**MUST NOT** hold a lock, transaction, or connection across network calls, disk I/O, or any operation with unbounded latency.

**Why:** One slow dependency then stalls every caller waiting on the lock, turning a latency blip into a system-wide outage.

**Detect:** grep lock scopes (`synchronized`, `with lock:`, `SELECT ... FOR UPDATE`, `BEGIN`) that enclose HTTP clients, file reads, or message publishes.

**References:** SEI CERT Oracle Coding Standard for Java, https://wiki.sei.cmu.edu/confluence/display/java/SEI+CERT+Oracle+Coding+Standard+for+Java

# No Preallocation From Declared Length

**MUST NOT** size buffers, vectors, or collections from a length the untrusted caller declares before the corresponding data arrives.

**Why:** Reserving a declared length up front lets one small request allocate gigabytes, and the validation happens after the memory is already committed.

**Detect:** grep with_capacity(, reserve(, new byte[, Buffer.alloc(, malloc( whose argument comes from a request field or deserialized header

**References:** Trail of Bits Testing Handbook, https://github.com/trailofbits/testing-handbook

# No Process Exit in Libraries

**MUST NOT** call process-exit primitives from library or handler code.

**Why:** An immediate exit skips every destructor, deferred call, and finally block, leaving locks held, buffers unflushed, and temp files behind.

**Detect:** grep os.Exit(, process.exit(, System.exit(, std::process::exit, die( outside main or entrypoint files

**References:** Trail of Bits Testing Handbook, https://github.com/trailofbits/testing-handbook

# No Silent Truncation

**MUST** reject values that exceed a fixed-size field or buffer instead of silently truncating security-relevant identifiers, paths, or hashes.

**Why:** A truncated identifier can collide with another principal or pass validation on a prefix while the consumer acts on the full intent.

**Detect:** grep fixed-size columns and slices on identifiers: `VARCHAR(16)`, `[:32]`, `substring(0,`, `strncpy(` on tokens, hashes, usernames, and paths.

**References:** SEI CERT C Coding Standard, https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard

# Off-by-One Errors

**MUST NOT** mix inclusive and exclusive bounds in loops, slices, pagination, and buffer sizes without a stated convention.

**Why:** A single misplaced `<` versus `<=` drops or duplicates records and can read one element past a buffer's end.

**Detect:** `range(len(x)-1)`, `i <= len(`, `arr[n]` where `n == len(arr)`, `LIMIT`/`OFFSET` arithmetic, `pageSize * page` mismatches.

**References:** CWE-193, CWE-119

# Complexity on Hot Paths & Quadratic Nested Loops (O(n²) on unbounded input)

**MUST NOT** nest loops over two externally sized collections without a bound on either dimension; **SHOULD** know the complexity of hot paths against realistic input sizes before shipping, not just correctness.

**Why:** A modest payload (10k × 10k) becomes 100M operations, letting one cheap request saturate CPU for everyone, and an unnoticed linear or worse scan inside a request turns moderate traffic into timeouts and CPU saturation.

**Detect:** `for ... for` over request arrays, `.map` inside `.filter` on user lists, join without index, no max-length on both sides; `in` membership on lists in loops, sort-then-scan per request, no complexity note on hot functions.

**References:** CWE-407, CWE-834, OWASP API DoS guidance, OWASP ASVS V11.1.3/V11.1.4

# Race Conditions

**MUST** guard shared-state mutations with proper synchronization (atomic ops, compare-and-set, or scoped locks) or immutability, never check-then-act on unsynchronized reads and never assume single-threaded execution.

**Why:** Interleaved read-modify-write across threads or nodes yields lost updates, double-spends, and intermittently corrupted data that surface only under production concurrency, carrying security holes that appear only under real load.

**Detect:** grep for `if (exists) then write`, `read(); modify(); write()` without CAS/`UPDATE ... WHERE version=`, non-atomic counters (`i++`), shared dict/list mutated without `Lock`/`mutex`/`synchronized`, cached mutable singletons, TOCTOU on file checks.

**References:** CWE-362 Race Condition, CWE-366, OWASP Race Condition guidance, NIST SP 800-53 SI-10, OWASP ASVS V11.1.6

# Storing Money as Floats

**MUST** represent currency as integers in minor units or an exact decimal type, never as binary floating point.

**Why:** Float rounding silently mis-charges customers, breaks reconciliation, and fails audit for financial records.

**Detect:** `float`/`double` in amount, price, balance, total columns or fields; `REAL`/`FLOAT` in migrations; `round(x*100)` casts.

**References:** CWE-1339, CWE-682, PCI DSS 6.5

# Strict Type Comparison

**MUST** validate that a value has the expected type and compare with strict equality at every trust boundary, never relying on implicit coercion.

**Why:** Type juggling makes an auth check pass for a value the author never imagined, such as an array or object satisfying a string comparison.

**Detect:** grep loose comparison in auth and validation paths: `==`/`!=` against request input, `in_array(` without the strict flag, `array_search` without strict.

**References:** OWASP ASVS v5.0 V15.3.5, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x24-V15-Secure-Coding-and-Architecture.md, CWE-843, CWE-697

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

# Uninitialized Memory Reads

**MUST NOT** read uninitialized memory on any path, including panic and early-exit paths between allocation and first write.

**Why:** A value always overwritten on the happy path is still observable when unwinding interrupts the sequence, leaking stale heap contents.

**Detect:** clippy MEM_REPLACE_WITH_UNINIT, or MSan on the C/C++ build

**References:** rust-clippy, https://github.com/rust-lang/rust-clippy

# Make Unsafe States Unrepresentable

**SHOULD** encode security-relevant state in types or schema constraints so illegal combinations cannot be constructed by a careless caller.

**Why:** Rules enforced by convention fail at the first forgotten check; rules enforced by the type system or schema fail at build time.

**Detect:** grep parallel boolean flags (`is_active`, `is_deleted`, `is_pending`), nullable `user_id`/`tenant_id` pairs, and status strings compared as free text.

**References:** NIST SP 800-218 SSDF, https://csrc.nist.gov/pubs/sp/800/218/final, Rust API Guidelines, https://rust-lang.github.io/api-guidelines/, Anderson, Security Engineering, https://www.cl.cam.ac.uk/~rja14/book.html

# Unsafe Code Confinement

**MUST** confine escape-hatch code to the smallest possible region, forbid it where unnecessary, and audit every remaining block.

**Why:** Memory-safety guarantees stop at the first unchecked block, and one unchecked pointer invalidates the argument for the whole module. A short reviewed list is auditable; scattered blocks are not.

**Detect:** command: `cargo geiger`, `#![forbid(unsafe_code)]` or `-D unsafe` lints, and `grep -rn unsafe` against a per-crate allowed list.

**References:** ANSSI Secure Rust Guidelines, https://anssi-fr.github.io/rust-guide/, Empirical study of Rust unsafe code (arXiv 2003.03296), https://arxiv.org/abs/2003.03296

# Use Standard Parsers

**SHOULD** use the platform's audited libraries for path, URL, and encoding handling instead of hand-rolled string splitting.

**Why:** Hand-rolled parsers rediscover the canonicalization and edge-case bugs the standard library already fixed, and disagree with the components downstream.

**Detect:** grep hand-rolled parsing: `split('/')` on paths, regex-based URL parsing, manual percent-decoding, and `indexOf('?')` query extraction.

**References:** OWASP Input Validation Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html

