#!/usr/bin/env python3
"""Merge discovery-agent candidate lists into topics.json.

Reads JSON arrays of {title, suggested_slug, suggested_categories, rationale}
from the given files, dedups against the existing topics.json (normalized title
and slug, plus difflib near-match >= 0.85), validates category names, and
either prints the surviving candidates (--dry-run, default) or appends them
with sequential numbers (--apply). Rejected/near-duplicate candidates are
recorded in scripts/discovery-rejected.json.
"""
import json
import re
import sys
import difflib
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
TOPICS = HERE / "topics.json"
REJECTED = HERE / "discovery-rejected.json"
VALID_CATS = None  # derived from topics.json at runtime


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def main() -> int:
    args = sys.argv[1:]
    apply = "--apply" in args
    files = [a for a in args if not a.startswith("--")]
    if not files:
        print("usage: merge_discovery.py [--dry-run|--apply] FILE [FILE...]", file=sys.stderr)
        return 2

    topics = json.loads(TOPICS.read_text())
    valid_cats = sorted({c for t in topics for c in t["categories"]})
    existing_titles = [norm(t["title"]) for t in topics]
    existing_slugs = {t["slug"] for t in topics}
    max_num = max(t["num"] for t in topics)

    candidates, rejected = [], []
    seen_titles = []
    for f in files:
        try:
            raw = json.loads(pathlib.Path(f).read_text())
        except (json.JSONDecodeError, OSError) as e:
            print(f"WARN: skipping {f}: {e}", file=sys.stderr)
            continue
        for c in raw:
            title = c.get("title", "").strip()
            slug = c.get("suggested_slug", "").strip().lower()
            cats = [x for x in c.get("suggested_categories", []) if x in valid_cats]
            nt = norm(title)
            if not title or not slug or not cats:
                rejected.append({**c, "reason": "missing title/slug/valid-category"})
                continue
            if slug in existing_slugs:
                rejected.append({**c, "reason": f"slug exists: {slug}"})
                continue
            close = [t for t in existing_titles + seen_titles
                     if difflib.SequenceMatcher(None, nt, t).ratio() >= 0.85]
            if close:
                rejected.append({**c, "reason": f"near-duplicate of: {close[0]}"})
                continue
            seen_titles.append(nt)
            candidates.append(c)

    rejected_path = REJECTED
    old_rejected = json.loads(rejected_path.read_text()) if rejected_path.exists() else []
    rejected_path.write_text(json.dumps(old_rejected + rejected, indent=2) + "\n")

    if not apply:
        print(f"{len(candidates)} surviving candidates "
              f"({len(rejected)} rejected -> discovery-rejected.json):\n")
        for i, c in enumerate(candidates, max_num + 1):
            print(f"{i}. {c['title']} [{', '.join(c['suggested_categories'])}] — {c.get('rationale','')}")
        print("\nRe-run with --apply (or edit this script's input) to merge approved items.")
        return 0

    for c in candidates:
        max_num += 1
        topics.append({"num": max_num, "title": c["title"],
                      "slug": c["suggested_slug"], "categories": c["suggested_categories"]})
    TOPICS.write_text(json.dumps(topics, indent=2) + "\n")
    print(f"Applied {len(candidates)} items. Total now {len(topics)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
