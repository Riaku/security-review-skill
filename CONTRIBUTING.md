# Contributing

Content corrections and new items are the point of this repo — most useful PRs
are one item added, one item made sharper, or one bad citation replaced.

`AGENTS.md` holds the full rules (written for AI agents and humans alike). The
short version:

## Adding or changing an item

1. One file per item: `issues/<slug>.md`. The YAML frontmatter (`categories:`,
   `domains:`, both sorted) is the **only** place membership is recorded — there
   is no index to update.
2. Keep the house shape: H1 title of five words or fewer, then one statement in
   a single BCP 14 keyword, then `**Why:**`, `**Detect:**` and `**References:**`.
   The statement is one obligation, not two — if the Detect line would have to
   check two different things, it is two items.
3. Keep it language-neutral. A source may be about Rust, Rails or a specific
   vendor; the item must read as a rule for any stack. Over-specific rules are
   rejected in review.
4. `**Detect:**` is one of three kinds, and must name an artifact a reviewer can
   inspect: a grep pattern, a named command, or a judgment (rare, and state what
   it reads). "Check for good security" is not a Detect line.
5. References: at most four, and each must actually support the rule. Fetch the
   URL before submitting — moved and invented links are the most common defect
   in contributed items.

## Before opening a PR

```bash
python3 scripts/check_generated.py   # FIRST: report bundles that no longer match
python3 scripts/gen_artifacts.py     # then write every bundle from the frontmatter
python3 scripts/check_generated.py   # must print: bundles-in-sync
```

Both scripts must exit 0, in that order — `check_generated.py` runs the generator
itself, so generating first would hide the drift it looks for. The last line must
read `bundles-in-sync: 35 bundles OK` (the count grows if a category is added).

Then:

- branch per change (`content/<category>`, `fix/<slug>`, `docs/<slug>`, `feat/<slug>`);
  `main` is protected and takes squash-merged PRs only
- Conventional Commit subject, 50 characters or fewer, imperative
- PR body with a Summary, a Test plan quoting the real generator output, and any
  Deferred items

## Licence

Contributions are accepted under the repository's [MIT licence](LICENSE.md):
inbound equals outbound. Do not paste text you do not have the right to license
this way — paraphrase the rule and cite the source instead, which is what the
items do already.

Inbound is enforced, not just stated: **every commit must be signed off**
(`git commit -s`), which is what the Developer Certificate of Origin means — you
are asserting you have the right to submit the change under this licence. CI
checks each PR commit for a `Signed-off-by` trailer matching the author, and
fails without one. Configure it once so you cannot forget:

```bash
git config --global format.signOff true
```

## Security

Do not open a public issue for a workflow, script or supply-chain vulnerability.
Use private reporting as described in [SECURITY.md](SECURITY.md).
