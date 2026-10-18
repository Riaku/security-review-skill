# Tree Traversal — Autonomous "What Is Met" Evaluation

Adapted from the frontier-round pattern in Matt Pocock's `grilling` skill,
with the question-asking removed: the frontier is *evaluated* against the
codebase instead of *asked* to a human. Use this as the mental model for
Phases 1–3.

## The tree

- **Root** — the target repo.
- **Domain nodes** (8) — settled by detection signals in `domains/*.md`.
  A domain is *settled* when you have inspected the repo and recorded
  applies / not-applies (with the signal that decided it).
- **Category nodes** (29) — settled by the domain's stack quick-map.
  A category is *unblocked* when at least one applying domain lists it.
- **Leaf nodes** (557 issues) — each `issues/<slug>.md` is a leaf hanging
  off its category. A leaf is *evaluable* when its category is unblocked.

## Work in rounds, not one giant pass

The **frontier** is every leaf whose category is unblocked right now.
Evaluate the whole frontier in one round — dispatch each unblocked category
to a sub-agent (or read its `bundles/<category>.md` directly), never
serially when the harness allows parallelism. Cap concurrency (≤2 heavy
sub-agents is a safe default on modest hardware).

Each round's verdicts reshape the tree:

- A verdict (`pass` / `fail` / `not-applicable`) **settles** the leaf.
  Nothing downstream re-opens it.
- A `needs-human` verdict is an **unsettled node**: record it, do not
  guess, and do not let downstream summaries treat it as settled.
- Cross-cutting discoveries mid-round (e.g. "this repo also has a mobile
  app") are **new facts that unblock new branches**: settle the new domain,
  recompute the frontier, fold the newly unblocked categories into the
  next round.

Recompute the frontier after every round. A leaf whose category only
becomes unblocked mid-review belongs to a *later* round, not this one.

## Facts are the agent's job, never the user's

Never ask the human for anything you can read, grep, or scan yourself.
Dispatch exploration (sub-agents, greps, tool runs from
`references/tooling.md`) and keep evaluating the rest of the frontier
while it runs — only questions downstream of a running exploration wait.
The only legitimate human input is the Phase 1 domain override and the
final `needs-human` list.

## Done when the frontier is empty

Every leaf visited: each has a verdict or is explicitly `needs-human`.
Nothing silently assumed — a category that was never dispatched is a bug
in the traversal, not a clean result. Then render the report; the review
is a shared-understanding artifact, not an action order: do not fix the
repo unless the user asks.
