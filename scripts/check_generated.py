#!/usr/bin/env python3
"""Check that generated artifacts are in sync with their sources.

Runs gen_manifests.py, then fails if any tracked generated file differs from
what the generator produces:

  domains/, categories/, bundles/, references/tool-index.md   (whole file)
  issues/*.md                                                 (nav footer only)

Issue files are canonical content, but the generator owns their trailing
"**Part of:**" navigation footer, so a stale footer (item refiled into another
category without re-running the generator) shows up here too. Run before
committing; CI enforces it.
"""
import subprocess
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

GENERATED_DIRS = ["domains", "categories", "bundles"]
GENERATED_FILES = ["references/tool-index.md"]
# Generator rewrites only the trailing nav footer block inside these files.
NAV_DIRS = ["issues"]


def main() -> int:
    before = {}
    paths = []
    for d in GENERATED_DIRS + NAV_DIRS:
        paths += sorted((ROOT / d).glob("*.md"))
    for f in GENERATED_FILES:
        p = ROOT / f
        if p.exists():
            paths.append(p)
    for p in paths:
        before[p] = p.read_text()

    subprocess.run([sys.executable, str(ROOT / "scripts" / "gen_manifests.py")],
                   check=True, stdout=subprocess.DEVNULL)

    drifted = [p.relative_to(ROOT) for p in paths
               if p.read_text() != before[p]]
    # also catch newly generated files not previously present
    now = set()
    for d in GENERATED_DIRS:
        now |= set((ROOT / d).glob("*.md"))
    for f in GENERATED_FILES:
        p = ROOT / f
        if p.exists():
            now.add(p)
    drifted += sorted(now - set(paths))

    nav_dirs = tuple(d + "/" for d in NAV_DIRS)
    if drifted:
        print("DRIFT: generated files are stale — re-run "
              "python3 scripts/gen_manifests.py and commit:")
        for d in drifted:
            note = "  (nav footer only, item body untouched)" \
                if str(d).startswith(nav_dirs) else ""
            print(f"  {d}{note}")
        return 1
    print(f"generated-in-sync: {len(paths)} files OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
