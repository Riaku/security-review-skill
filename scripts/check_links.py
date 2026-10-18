#!/usr/bin/env python3
"""Link checker for the skill repo — it walks *three* link graphs.

  1. The **network graph**: external `http`/`https` links. Every http(s) URL
     found in a ``*.md`` file is fetched (HEAD, then GET on 403/405/501) and
     reported when it does not resolve. This needs the internet, so it is
     skipped entirely under ``--offline``. Placeholder/example URLs are skipped
     by pattern because they document attack targets rather than real
     references. A 403/429 is treated as WAF bot-blocking (WARN), not link rot.

  2. The repo's own **relative link graph**, as *resolution*. Every markdown
     link ``[label](t)`` or image ``![alt](t)`` whose target ``t`` is a
     relative path must resolve to a file or directory that exists on disk.
     This mirrors the structural checks in ``validate_skill.py`` but is
     generic: it follows *any* relative link, so a stale cross-reference
     (issue <-> category <-> domain <-> SKILL.md) fails here even when it is not
     one of the manifests ``validate_skill.py`` parses. No network, so it runs
     in both normal and ``--offline`` mode.

  3. The repo's own **relative link graph**, as *structure*: a breadth-first
     crawl from ``SKILL.md`` (``linkgraph.crawl``) that checks the tree is
     still *navigable*, not merely *resolvable* — which documents are reachable
     from the entry point, which are orphaned (no path reaches them at all),
     and whether the navigation claims round-trip: a category manifest lists an
     issue <=> that issue's ``**Part of:**`` footer links back; a domain
     manifest lists a category <=> that category's ``Domain:`` line points
     back. Every document under ``issues/ categories/ domains/ references/
     templates/ bundles/`` must be reachable; ``SKILL.md``, ``AGENTS.md`` and
     ``SOURCES.md`` are the only documents allowed to have no inbound link, and
     a document in the hand-authored ``references/`` or ``templates/`` must be
     *named* by an inbound link — being swept up by a directory link is not
     enough for those two. Also offline: it only reads the working tree.

Link *extraction* — masking fenced code blocks (``` / ~~~) and inline code
spans, resolving a relative target, classifying a target as a repo path or not
— lives in exactly one place: ``scripts/linkgraph.py``. This module imports it
(``lg``) and ``scripts/manifest_links.py`` (``ml``) for the canonical manifest
and footer forms instead of re-implementing either.

Exit status is 1 when any of the three graphs is broken — external-broken,
relative-broken, orphaned document, round-trip inconsistency, or a broken edge
found by the crawl — and 0 when all three are clean.

Usage:
  python3 scripts/check_links.py            # external URLs + relative + crawl
  python3 scripts/check_links.py --offline  # relative + crawl only
"""
from __future__ import annotations

import pathlib
import re
import sys
import urllib.error
import urllib.request
from typing import NamedTuple

import linkgraph as lg
import manifest_links as ml

ROOT = pathlib.Path(__file__).resolve().parent.parent

# --- graph 1: external http(s) URLs ----------------------------------------

URL_RE = re.compile(r'https?://[^\s)\]>"\'`]+')

# Placeholders: examples, attack-target illustrations, template vars,
# link-local metadata IPs — never fetched.
SKIP_PATTERNS = [
    r'\.<',            # https://mta-sts.<domain>
    r'\{',             # template vars
    r'example\.',      # example.com etc.
    r'\bphish',        # phishing illustration URLs
    r'169\.254\.',     # link-local (IMDS example)
    r'\bx\.com/ghumare64/status',  # social post, often blocks bots (checked manually)
    r'localhost',
    r'\.internal\b',
    r'\.\.\.',         # truncated URLs
    r'^http://app$',   # nginx proxy_pass example in hsts.md
    r'token\.actions\.githubusercontent\.com',  # OIDC issuer value, not a browsable page
]

UA = {"User-Agent": "Mozilla/5.0 (compatible; skill-link-checker)"}


def is_placeholder(url: str) -> bool:
    return any(re.search(p, url) for p in SKIP_PATTERNS)


def fetch_ok(url: str) -> tuple[str, str]:
    """Returns ('ok'|'blocked'|'broken', status)."""
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, method=method, headers=UA)
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return "ok", str(r.status)
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (403, 405, 501):
                continue  # try GET
            # 403/429 from datacenter IPs is WAF bot-blocking, not link rot.
            if e.code in (403, 429):
                return "blocked", str(e.code)
            return "broken", str(e.code)
        except Exception as e:
            return "broken", type(e).__name__
    return "broken", "unreachable"


# --- graph 2: relative-link resolution -------------------------------------


def check_relative(files) -> tuple[int, list[tuple[str, int, str]], int]:
    """Validate every relative markdown link in `files`.

    Returns (checked, broken, skipped) where `broken` is a list of
    (relative_file, line_no, raw_target) and `skipped` counts targets that are
    not repo-relative paths (anchors, schemes, absolute, placeholders).

    Extraction is ``linkgraph.iter_links`` — the same crawler the structural
    checks below use, so there is one implementation of masking/title-stripping
    /classification. It yields only the *relative* targets, so the non-relative
    ones are whatever is left when its output is subtracted from the raw link
    matches; that keeps the reported counts identical to the hand-rolled pass
    this replaced.
    """
    checked = 0
    skipped = 0
    broken = []
    for f in files:
        text = f.read_text(encoding="utf-8", errors="ignore")
        links = list(lg.iter_links(f, text))
        checked += len(links)
        matches = sum(1 for _ in lg.LINK_RE.finditer(lg.mask_code(text)))
        skipped += matches - len(links)
        for ln in links:
            if not ln.path.exists():
                broken.append((str(f.relative_to(ROOT)), ln.line, ln.target))
    return checked, broken, skipped


# --- graph 3: the link graph as a structure --------------------------------

# A document that no crawl path reaches is unreachable. The navigation graph
# lives in issues/ categories/ domains/ references/ templates/ bundles/ (every
# navigation target sits one level below the root — see manifest_links.py), and
# reachability includes *directory-link expansion*: ``[issues/](../issues/)``
# pulls in every direct ``*.md`` of that directory, so a stray document dropped
# directly inside one of those dirs is still reached, while one placed in a
# subdirectory — or at the root — is not.
#
# Root-level documents allowed to have *no* inbound link. SKILL.md is where the
# crawl starts, so nothing needs to point back at it; AGENTS.md, SOURCES.md and
# README.md are agent/attribution/entry-point housekeeping rather than part of
# the navigable tree (they are not targets of the cross-linking every other
# document does). Every other unreachable document fails the run.
ROOT_EXEMPT = ("SKILL.md", "AGENTS.md", "SOURCES.md", "README.md")

# Hand-authored directories hold documents a human wrote, so each one must be
# *named* by an inbound link: reachability through a directory link is not
# enough for them, or a document dropped in alongside would silently ride along
# on that directory's expansion. Generated directories (issues/ categories/
# domains/ bundles/) are the opposite — their hundreds of files are covered by
# the directory links in SKILL.md and are never named individually.
NAMED_DIRS = ("references", "templates")


class RoundTrip(NamedTuple):
    """Reciprocal navigation claims, checked over a crawl."""
    cat_consistent: int
    dom_consistent: int
    # (file, target, why): the link missing from `file`
    cat_bad: list[tuple[pathlib.Path, pathlib.Path, str]]
    dom_bad: list[tuple[pathlib.Path, pathlib.Path, str]]


def check_round_trip(c: lg.Crawl) -> RoundTrip:
    """Check that the navigation claims between documents are reciprocal.

    Driven by the crawl — candidate documents and their links come from
    ``c.docs`` / ``c.edges``, reachability from ``c.reached`` — with the
    canonical forms taken from ``manifest_links`` (``CAT_ITEM_RE`` /
    ``DOMAIN_ITEM_RE`` for manifest list items, ``footer_of`` plus
    ``category_link`` / ``domain_link`` for the issue footer and the category
    header). Two directions:

    category <-> issue
        every issue a category manifest links to must name that category in
        its ``**Part of:**`` footer line, and every category named in such a
        footer must be one that lists that issue.

    domain <-> category
        every category a ``domains/*.md`` manifest lists must exist as a
        *reachable* ``categories/<cat>.md``, and every category's ``Domain:``
        line must point at a domain manifest that lists it back.
    """
    cats_dir = c.root / "categories"
    issues_dir = c.root / "issues"
    doms_dir = c.root / "domains"
    text_cache: dict[pathlib.Path, str] = {}

    def text_of(doc: pathlib.Path) -> str:
        if doc not in text_cache:
            text_cache[doc] = doc.read_text(encoding="utf-8", errors="ignore")
        return text_cache[doc]

    def listed(doc: pathlib.Path, item_re, directory: pathlib.Path) -> list[pathlib.Path]:
        """The canonical list items of `doc`, as resolved paths.

        The *claim* a manifest makes is its list-item line
        (``- [slug](../issues/slug.md)`` / ``- [cat](../categories/cat.md)``);
        the same target mentioned in prose (a domain's "Stack quick-map", which
        deliberately cross-references other domains' categories) is a
        resolution-checked link, not an ownership claim, so it is not part of
        the round trip.
        """
        return [(directory / f"{stem}.md").resolve()
                for stem in ml.manifest_items(doc, item_re)]

    # --- category manifests: the issues each one lists ----------------------
    listed_by_cat: dict[pathlib.Path, list[pathlib.Path]] = {}
    for doc in c.docs:
        if doc.parent == cats_dir:
            listed_by_cat[doc] = listed(doc, ml.CAT_ITEM_RE, issues_dir)

    # --- issue footers: the categories each one names ----------------------
    named_by_issue: dict[pathlib.Path, set[pathlib.Path]] = {}
    for doc in c.docs:
        if doc.parent != issues_dir:
            continue
        named: set[pathlib.Path] = set()
        footer = ml.footer_of(text_of(doc))
        if footer is not None:
            # Only links *inside* the footer line count as the back-link.
            for ln in lg.iter_links(doc, footer):
                if ln.path.parent == cats_dir and ln.path.suffix == ".md":
                    named.add(ln.path)
        named_by_issue[doc] = named

    # --- domain manifests: the categories each one lists -------------------
    listed_by_dom: dict[pathlib.Path, list[pathlib.Path]] = {}
    for doc in c.docs:
        if doc.parent == doms_dir:
            listed_by_dom[doc] = listed(doc, ml.DOMAIN_ITEM_RE, cats_dir)

    # --- category headers: the domains each one points at -------------------
    # The nav line is `Domain: [x](../domains/x.md)` for a category whose items
    # all sit in one domain, `Domains: [x] · [y]` once they span several — an
    # item declares its own domains, so a category rolls them up.
    dom_of_cat: dict[pathlib.Path, set[pathlib.Path]] = {}
    for doc in c.docs:
        if doc.parent != cats_dir:
            continue
        line = next((ln for ln in text_of(doc).splitlines()
                     if ln.startswith(("Domain:", "Domains:"))), None)
        doms: set[pathlib.Path] = set()
        if line is not None:
            for ln in lg.iter_links(doc, line):
                if ln.path.parent == doms_dir and ln.path.suffix == ".md":
                    doms.add(ln.path)
        dom_of_cat[doc] = doms

    cat_bad: list[tuple[pathlib.Path, pathlib.Path, str]] = []
    dom_bad: list[tuple[pathlib.Path, pathlib.Path, str]] = []

    # --- category <-> issue -------------------------------------------------
    cat_pairs = {(cat, iss)
                 for cat, issues in listed_by_cat.items() for iss in issues}
    cat_pairs |= {(cat, iss)
                  for iss, cats in named_by_issue.items() for cat in cats}
    cat_consistent = 0
    for cat, iss in sorted(cat_pairs, key=lambda p: (p[0].name, p[1].name)):
        if iss not in c.reached:
            cat_bad.append((cat, iss, "linked issue is not reachable"))
        elif iss not in listed_by_cat.get(cat, []):
            cat_bad.append((cat, iss,
                            "missing: category manifest does not list it"))
        elif cat not in named_by_issue.get(iss, set()):
            cat_bad.append((iss, cat, "missing: issue footer does not link back"))
        else:
            cat_consistent += 1

    # --- domain <-> category ------------------------------------------------
    dom_pairs = {(dom, cat)
                 for dom, cats in listed_by_dom.items() for cat in cats}
    dom_pairs |= {(dom, cat)
                  for cat, doms in dom_of_cat.items() for dom in doms}
    dom_consistent = 0
    for dom, cat in sorted(dom_pairs, key=lambda p: (p[0].name, p[1].name)):
        if cat not in c.reached:
            dom_bad.append((dom, cat, "listed category is not reachable"))
        elif dom not in c.reached:
            dom_bad.append((cat, dom, "pointed-at domain is not reachable"))
        elif cat not in listed_by_dom.get(dom, []):
            dom_bad.append((dom, cat,
                            "missing: domain manifest does not list it"))
        elif dom not in dom_of_cat.get(cat, set()):
            dom_bad.append((dom, cat,
                            "missing: category Domain: line does not point back"))
        else:
            dom_consistent += 1

    return RoundTrip(cat_consistent, dom_consistent, cat_bad, dom_bad)


def main() -> int:
    offline = "--offline" in sys.argv
    files = sorted(p for p in ROOT.rglob("*.md")
                   if ".git" not in p.parts)

    # --- graph 2: the repo's own relative links (no network, always runs) ---
    rel_checked, rel_broken, rel_skipped = check_relative(files)

    # --- graph 1: external http(s) URLs ------------------------------------
    urls = {}
    for f in files:
        for m in URL_RE.finditer(f.read_text(encoding="utf-8", errors="ignore")):
            u = m.group(0).rstrip(".,;:")
            urls.setdefault(u, set()).add(str(f.relative_to(ROOT)))

    real = {u: v for u, v in urls.items() if not is_placeholder(u)}
    skipped = len(urls) - len(real)
    broken = []
    blocked = []
    if not offline:
        for u in sorted(real):
            state, status = fetch_ok(u)
            mark = {"ok": "ok ", "blocked": "WARN", "broken": "FAIL"}[state]
            print(f"  {mark} {status:>4}  {u}")
            if state == "broken":
                broken.append((u, status, sorted(real[u])))
            elif state == "blocked":
                blocked.append(u)
    else:
        print(f"offline mode: {len(real)} real URLs would be checked")

    print(f"\nlinks: {len(real)} checked, {skipped} placeholders skipped, "
          f"{len(blocked)} WAF-blocked (not treated as broken), "
          f"{len(broken)} broken")
    print(f"relative links: {rel_checked} checked, {len(rel_broken)} broken"
          + (f" ({rel_skipped} non-relative/placeholder targets skipped)"
             if rel_skipped else ""))
    for u, status, where in broken:
        print(f"  BROKEN {status}: {u}")
        for w in where:
            print(f"    in {w}")
    for rel, line, target in rel_broken:
        print(f"  {rel}:{line} -> {target}")

    # --- graph 3: the same links as a structure (crawl, always runs) -------
    c = lg.crawl(start=ROOT / "SKILL.md", root=ROOT)
    reachable = len(c.reached)
    orphans = c.orphans(exempt=ROOT_EXEMPT)
    # Hand-authored documents must be *named*, not merely swept up by a
    # directory link (see NAMED_DIRS).
    hand = [p for p in sorted(c.all_docs()) if p.parent.name in NAMED_DIRS]
    unnamed = [p for p in hand
               if not any(ln.source != p for ln in c.inbound(p))]
    rt = check_round_trip(c)

    print(f"link graph: {reachable} documents reachable from "
          f"{c.start.relative_to(ROOT)}, {len(orphans)} unreachable")
    print(f"  exempt (no inbound link required, root-level): "
          f"{', '.join(ROOT_EXEMPT)}")
    for p in orphans:
        print(f"  UNREACHABLE {p.relative_to(ROOT)}")
    print(f"hand-authored links: {len(hand) - len(unnamed)} named, "
          f"{len(unnamed)} unnamed")
    for p in unnamed:
        print(f"  UNNAMED {p.relative_to(ROOT)} (reached only by directory "
              f"expansion — link it from SKILL.md or another document)")
    print(f"round-trip: {rt.cat_consistent} category<->issue pairs consistent, "
          f"{len(rt.cat_bad)} inconsistent")
    print(f"round-trip: {rt.dom_consistent} domain<->category pairs consistent, "
          f"{len(rt.dom_bad)} inconsistent")
    for src, tgt, why in (*rt.cat_bad, *rt.dom_bad):
        print(f"  {src.relative_to(ROOT)} -> {tgt.relative_to(ROOT)} ({why})")
    # Already failed by the resolution pass above; named here so a document
    # that is linked-but-absent can never slip through unnoticed, and *not*
    # added to any of the summary counts above.
    print(f"crawl: {len(c.broken)} broken edges")
    for ln in c.broken:
        print(f"  BROKEN EDGE {ln.source.relative_to(ROOT)}:{ln.line} -> "
              f"{ln.target}")

    return 1 if (broken or rel_broken or orphans or unnamed or rt.cat_bad
                 or rt.dom_bad or c.broken) else 0


if __name__ == "__main__":
    raise SystemExit(main())
