#!/usr/bin/env python3
"""Generate scripts/topics.json by parsing the taxonomy tables from the plan file.

The plan file is the authoring source of truth; topics.json is the machine
coverage source of truth. Re-running this after plan edits keeps them in sync.
"""
import json
import re
import sys
import pathlib

if len(sys.argv) > 1:
    PLAN = pathlib.Path(sys.argv[1])
else:
    sys.exit("usage: gen_topics.py <planning-doc.md>")
OUT = pathlib.Path(__file__).resolve().parent / "topics.json"

ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([a-z0-9-]+)\s*\|\s*([^|]+?)\s*\|$")
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

def main() -> int:
    items = {}
    for line in PLAN.read_text().splitlines():
        m = ROW.match(line)
        if not m:
            continue
        num, title, slug, cats = m.groups()
        num = int(num)
        cats = [c.strip() for c in cats.split(",") if c.strip()]
        if not SLUG.match(slug):
            print(f"ERROR: bad slug {slug!r} for #{num}", file=sys.stderr)
            return 1
        if not cats:
            print(f"ERROR: no categories for #{num}", file=sys.stderr)
            return 1
        if num in items and items[num] != (title, slug, cats):
            print(f"ERROR: conflicting rows for #{num}", file=sys.stderr)
            return 1
        items[num] = (title, slug, cats)

    if 250 in items:
        print("ERROR: #250 must be dropped", file=sys.stderr)
        return 1
    topics = [{"num": n, "title": items[n][0], "slug": items[n][1],
               "categories": items[n][2]} for n in sorted(items)]
    slugs = [t["slug"] for t in topics]
    if len(set(slugs)) != len(slugs):
        print("ERROR: duplicate slugs", file=sys.stderr)
        return 1
    OUT.write_text(json.dumps(topics, indent=2) + "\n")
    print(f"Wrote {len(topics)} topics to {OUT.name}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
