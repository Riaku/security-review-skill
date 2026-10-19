#!/usr/bin/env python3
"""Fail if a committed bundle differs from what the generator produces.

``bundles/*.md`` are the only generated files in this repository, and each one
is generated whole, so the check is a straight before/after comparison:
snapshot the bundles, run ``scripts/gen_artifacts.py``, re-read, and report
every bundle whose contents changed or that appeared for the first time.

Nothing else in the tree is compared, because nothing else is generated: an
item's body, a category's overview and a domain's signals are authored, and
editing them is not drift.

Exit codes:
  0  every bundle matches the generator's output
  1  at least one bundle drifted, or the generator itself failed

Run before committing; CI enforces it.
"""
from __future__ import annotations

import difflib
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GENERATOR = ROOT / "scripts" / "gen_artifacts.py"
BUNDLES_DIR = ROOT / "bundles"

# Cap on the unified-diff lines printed per drifting bundle.
DIFF_LINES = 12


def bundles() -> list[pathlib.Path]:
    """Every ``bundles/*.md``, sorted."""
    return sorted(p for p in BUNDLES_DIR.glob("*.md") if p.is_file())


def diff_of(before: str, after: str) -> list[str]:
    """Indented unified-diff lines between the on-disk and generated bundle."""
    lines = list(difflib.unified_diff(
        before.splitlines(), after.splitlines(),
        fromfile="on disk", tofile="generated", lineterm="", n=1))[2:]
    if len(lines) > DIFF_LINES:
        lines = lines[:DIFF_LINES] + [
            f"... {len(lines) - DIFF_LINES} more diff line(s)"]
    return [f"    {line}" for line in lines]


def main() -> int:
    paths = bundles()
    before = {p: p.read_text(encoding="utf-8") for p in paths}

    result = subprocess.run([sys.executable, str(GENERATOR)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                            text=True)
    if result.returncode != 0:
        # The generator is the format gate and its own message is the useful
        # one, so surface that instead of a CalledProcessError traceback.
        print("the generator failed — fix that first, then re-run this check:")
        error = (result.stderr or "").strip()
        print(f"  {error}" if error else
              f"  {GENERATOR.relative_to(ROOT)} exited {result.returncode}")
        return 1

    drifted = []
    for p in paths:
        after = p.read_text(encoding="utf-8")
        if after != before[p]:
            drifted.append((p, before[p], after))
    # A bundle the generator just created has no snapshot to compare against —
    # report it rather than letting it ride in uncommitted.
    created = [p for p in bundles() if p not in before]

    if not drifted and not created:
        print(f"bundles-in-sync: {len(paths)} bundles OK")
        return 0

    print("DRIFT: bundles are stale — re-run "
          "`python3 scripts/gen_artifacts.py` and commit:")
    for p, was, now in drifted:
        print(f"  {p.relative_to(ROOT)}")
        for line in diff_of(was, now):
            print(line)
    for p in created:
        print(f"  {p.relative_to(ROOT)}  (new bundle, not committed)")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
