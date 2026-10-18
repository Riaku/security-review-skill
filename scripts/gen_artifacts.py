#!/usr/bin/env python3
"""Generate the skill's derived artifacts from the documents themselves.

There is no taxonomy table anywhere. Each item's frontmatter is the single
source of category/domain membership:

    issues/<slug>.md   ---
                       categories: [a, b]
                       domains: [c]
                       ---

                       # Title
                       ...authored body...

                       ---

                       **Part of:** ...        (generated nav footer)

Everything else is derived, in one pass, from that frontmatter and from the
relative link graph:

  issues/*.md          regenerated trailing "**Part of:**" nav footer only
  categories/*.md      generated "## Issues" tail (its items, then its domains)
  domains/*.md         generated "## Categories" tail (its categories)
  bundles/*.md         fully generated: every item of a category inlined

Derivations
    item -> (categories, domains)   ml.item_meta(text)
    category -> items               every issue naming it, sorted by slug
    category -> domains             union of its items' domains, sorted
    domain -> categories            every category with >=1 item naming it

The manifests and footers written here *are* the graph the bundles are then
assembled from: before a single bundle is written this script crawls the
relative link graph from SKILL.md (scripts/linkgraph.py) and refuses to
continue on a broken edge, a category manifest the crawl never reaches, or an
issue file the crawl never reaches — naming the offenders. Each bundle's item
order is the issue links its ``categories/<cat>.md`` manifest lists, and each
body is read from the path that link resolves to, with the frontmatter
stripped.

Layout (see scripts/manifest_links.py): every navigation target sits exactly
one directory below the repo root, so ``../<dir>/<file>.md`` is correct from
every document type.

Idempotent: a second run with no authored change rewrites byte-identical
files. Detection signals, scopes and stack quick-maps are authored in the
documents; nothing here keeps a copy.
"""
from __future__ import annotations

import pathlib
import sys

import linkgraph as lg
import manifest_links as ml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL_FILE = ROOT / "SKILL.md"
ISSUES_DIR = ROOT / "issues"
CATEGORIES_DIR = ROOT / "categories"
DOMAINS_DIR = ROOT / "domains"
BUNDLES_DIR = ROOT / "bundles"


class BuildError(Exception):
    """A condition the generator refuses to write through (exit 1)."""


def _md_files(directory: pathlib.Path) -> list[pathlib.Path]:
    """Sorted *.md files directly inside `directory`."""
    return sorted(p for p in directory.glob("*.md") if p.is_file())


def load_items() -> dict[str, dict[str, list[str]]]:
    """Parse every issues/*.md frontmatter; raise BuildError if malformed."""
    items: dict[str, dict[str, list[str]]] = {}
    for path in _md_files(ISSUES_DIR):
        try:
            items[path.stem] = ml.item_meta(path.read_text())
        except ValueError as exc:
            raise BuildError(
                f"{path.relative_to(ROOT)}: malformed frontmatter — {exc}"
            ) from exc
    return items


def check_manifests(items: dict[str, dict[str, list[str]]]) -> None:
    """Every category/domain named in frontmatter must have a manifest file."""
    known_cats = {p.stem for p in _md_files(CATEGORIES_DIR)}
    known_doms = {p.stem for p in _md_files(DOMAINS_DIR)}
    for slug in sorted(items):
        meta = items[slug]
        for cat in meta["categories"]:
            if cat not in known_cats:
                raise BuildError(
                    f"issues/{slug}.md names category {cat!r}, but "
                    f"categories/{cat}.md does not exist")
        for dom in meta["domains"]:
            if dom not in known_doms:
                raise BuildError(
                    f"issues/{slug}.md names domain {dom!r}, but "
                    f"domains/{dom}.md does not exist")


def cat_items(items: dict[str, dict[str, list[str]]]) -> dict[str, list[str]]:
    """category -> its item slugs, sorted by slug."""
    out: dict[str, list[str]] = {}
    for slug, meta in items.items():
        for cat in meta["categories"]:
            out.setdefault(cat, []).append(slug)
    return {cat: sorted(slugs) for cat, slugs in out.items()}


def cat_domains(items: dict[str, dict[str, list[str]]]) -> dict[str, set[str]]:
    """category -> union of its items' domains."""
    out: dict[str, set[str]] = {}
    for meta in items.values():
        for cat in meta["categories"]:
            out.setdefault(cat, set()).update(meta["domains"])
    return out


def domain_cats(items: dict[str, dict[str, list[str]]]) -> dict[str, set[str]]:
    """domain -> every category with >=1 item naming that domain."""
    out: dict[str, set[str]] = {}
    for meta in items.values():
        for dom in meta["domains"]:
            out.setdefault(dom, set()).update(meta["categories"])
    return out


def scope_of(text: str) -> str:
    """First non-empty line after the H1 of a manifest (its scope paragraph)."""
    seen_h1 = False
    for line in text.splitlines():
        stripped = line.strip()
        if not seen_h1:
            if stripped.startswith("# "):
                seen_h1 = True
            continue
        if stripped:
            return stripped
    return ""


def write_footers(items: dict[str, dict[str, list[str]]]) -> int:
    """Regenerate only the trailing nav footer of every issue file."""
    written = 0
    for slug, meta in items.items():
        path = ISSUES_DIR / f"{slug}.md"
        text = path.read_text()
        updated = ml.with_footer(text, meta["categories"], meta["domains"])
        if updated != text:
            path.write_text(updated)
        written += 1
    return written


def write_category_tails(items: dict[str, dict[str, list[str]]]) -> tuple[int, dict[str, str]]:
    """Write each category's `## Issues` tail; also capture its scope paragraph."""
    items_by_cat = cat_items(items)
    doms_by_cat = cat_domains(items)
    scopes: dict[str, str] = {}
    for path in _md_files(CATEGORIES_DIR):
        cat = path.stem
        text = path.read_text()
        scopes[cat] = scope_of(text)
        tail = ml.render_category_tail(items_by_cat.get(cat, []),
                                       doms_by_cat.get(cat, set()))
        path.write_text(ml.with_tail(text, ml.CAT_TAIL_HEAD, tail))
    return len(scopes), scopes


def write_domain_tails(items: dict[str, dict[str, list[str]]]) -> int:
    """Write each domain's `## Categories` tail."""
    cats_by_dom = domain_cats(items)
    for path in _md_files(DOMAINS_DIR):
        text = path.read_text()
        tail = ml.render_domain_tail(cats_by_dom.get(path.stem, set()))
        path.write_text(ml.with_tail(text, ml.DOM_TAIL_HEAD, tail))
    return len(_md_files(DOMAINS_DIR))


def _rel(path: pathlib.Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def assert_coverage(crawl: lg.Crawl) -> None:
    """Refuse to write any bundle unless the crawl reaches the whole tree."""
    if crawl.broken:
        offenders = "; ".join(
            f"{_rel(ln.source)}:{ln.line} -> {ln.target}" for ln in crawl.broken)
        raise BuildError(
            f"crawl from SKILL.md found {len(crawl.broken)} broken link(s): "
            f"{offenders}")

    reached = crawl.reached

    unreached_cats = [p for p in _md_files(CATEGORIES_DIR)
                      if p.resolve() not in reached]
    if unreached_cats:
        names = ", ".join(_rel(p) for p in unreached_cats)
        raise BuildError(
            f"crawl from SKILL.md never reached {len(unreached_cats)} category "
            f"manifest(s): {names}")

    unreached_issues = [p for p in _md_files(ISSUES_DIR)
                        if p.resolve() not in reached]
    if unreached_issues:
        names = ", ".join(_rel(p) for p in unreached_issues[:20])
        more = "" if len(unreached_issues) <= 20 else (
            f" (and {len(unreached_issues) - 20} more)")
        raise BuildError(
            f"crawl from SKILL.md never reached {len(unreached_issues)} issue "
            f"file(s): {names}{more}")


def write_bundles(scopes: dict[str, str]) -> int:
    """Write one fully-generated bundle per categories/*.md, following links."""
    issues_dir = ISSUES_DIR.resolve()
    count = 0
    for path in _md_files(CATEGORIES_DIR):
        cat = path.stem
        manifest = path.resolve()
        slugs = lg.issue_slugs(manifest)
        item_path: dict[str, pathlib.Path] = {}
        for ln in lg.iter_links(manifest):
            if ln.path.parent == issues_dir and ln.path.suffix == ".md":
                item_path.setdefault(ln.path.stem, ln.path)
        missing = [s for s in slugs if s not in item_path]
        if missing:
            raise BuildError(
                f"categories/{cat}.md lists item(s) whose link target could "
                f"not be resolved: {', '.join(missing)}")
        parts = [f"# {cat} — full checklist ({len(slugs)} items)", "",
                 scopes.get(cat, ""), "",
                 "> Generated artifact — edit the issue files, not this one. "
                 f"Sources: {ml.ISSUES_DIR_LINK} · manifest: "
                 f"{ml.category_link(cat)} · index: {ml.SKILL_LINK}", ""]
        for slug in slugs:
            body = ml.strip_meta(item_path[slug].read_text()).rstrip()
            parts += [body, ""]
        (BUNDLES_DIR / f"{cat}.md").write_text("\n".join(parts) + "\n")
        count += 1
    return count


def main() -> int:
    if not SKILL_FILE.exists():
        raise BuildError("SKILL.md not found at the repo root")
    BUNDLES_DIR.mkdir(exist_ok=True)

    items = load_items()
    check_manifests(items)

    # The issue footers must carry the same category/domain links the bundles
    # will inline, so write them before the crawl and the bundles.
    n_footers = write_footers(items)
    n_cat_tails, scopes = write_category_tails(items)
    n_dom_tails = write_domain_tails(items)

    # The manifests and footers just written are the graph the bundles are
    # assembled from. Crawl it from SKILL.md and prove the tree is whole
    # before writing any bundle.
    crawl = lg.crawl()
    assert_coverage(crawl)

    n_bundles = write_bundles(scopes)

    print(f"wrote {n_bundles} bundles, {n_cat_tails} category tails, "
          f"{n_dom_tails} domain tails, {n_footers} footers from "
          f"{len(items)} items")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BuildError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
