# Unhandled Promise Rejections

**MUST** attach a rejection handler to every promise/async call, or register a global unhandled-rejection hook that fails loudly.

**Why:** An unhandled rejection can silently kill a worker or, in older Node versions, crash the process mid-request with no trace.

**Detect:** `.then(` without `.catch(`, `await` outside try/catch in entry points, missing `process.on('unhandledRejection')`, floating promises with no `void`.

**References:** CWE-584, CWE-248, Node.js unhandledRejection docs
