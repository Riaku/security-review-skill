#!/usr/bin/env python3
"""Check that every reference URL cited by an item still resolves.

Scope is deliberately narrow: only URLs on an item's `**References:**` line are
probed, because URLs elsewhere in an item are frequently deliberate examples
(`169.254.169.254`, `http://app`, `api.internal.example`).

Classification:
  ok       2xx (202 is tolerated: some publishers front-load a JS redirect)
  blocked  401/403/429 — the host refuses datacenter IPs, so "dead" cannot be
           concluded from here; these are reported but never fail the run
  broken   404/410/000 after a retry — a real finding

Exit code is 1 when anything is broken, so the scheduled workflow turns red and
notifies; the job is not a required check, so it never blocks a PR.
"""
from __future__ import annotations

import concurrent.futures
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ISSUES = ROOT / "issues"
UA = "security-review-skill-linkcheck/1.0 (+https://github.com/Riaku/security-review-skill)"
TIMEOUT = 25
WORKERS = 6
OK_CODES = set(range(200, 300)) - {202}
TOLERATED = {202}
BLOCKED = {401, 403, 429}
URL_RE = re.compile(r"https?://[^\s)\]>,`\"']+")


def urls_by_item() -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for path in sorted(ISSUES.glob("*.md")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.lstrip().startswith("**References:**"):
                continue
            for raw in URL_RE.findall(line):
                url = raw.rstrip(".,;:!?")
                found.setdefault(str(path.relative_to(ROOT)), []).append(url)
    return found


def probe(url: str) -> int | str:
    for attempt in (1, 2):
        req = urllib.request.Request(url, method="GET", headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return resp.status
        except urllib.error.HTTPError as exc:
            code = exc.code
            if attempt == 2 or code not in (0, 500, 502, 503, 504):
                return code
        except Exception:
            if attempt == 2:
                return 0
    return 0


def classify(code: int | str) -> str:
    if code in OK_CODES or code in TOLERATED:
        return "ok"
    if code in BLOCKED:
        return "blocked"
    return "broken"


def main() -> int:
    citations = urls_by_item()
    pairs = sorted({(item, url) for item, urls in citations.items() for url in urls})
    unique = sorted({url for _, url in pairs})
    print(f"{len(pairs)} citations of {len(unique)} unique URLs across {len(citations)} items")

    results: dict[str, int | str] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for url, code in zip(unique, pool.map(probe, unique)):
            results[url] = code

    broken = [(item, url, results[url]) for item, url in pairs if classify(results[url]) == "broken"]
    blocked = [(item, url, results[url]) for item, url in pairs if classify(results[url]) == "blocked"]

    for label, rows in (("BROKEN", broken), ("BLOCKED (host refuses datacenter IPs)", blocked)):
        if rows:
            print(f"\n{label}: {len(rows)}")
            for item, url, code in rows:
                print(f"  {code}  {item}  {url}")

    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        lines = [f"## Reference link check", "", f"- citations: **{len(pairs)}** ({len(unique)} unique)", f"- broken: **{len(broken)}**", f"- blocked hosts: {len(blocked)}", ""]
        if broken:
            lines += ["| item | code | url |", "|---|---|---|"]
            lines += [f"| `{item}` | {code} | {url} |" for item, url, code in broken]
        Path(summary).write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"\nbroken={len(broken)} blocked={len(blocked)} ok={len(pairs) - len(broken) - len(blocked)}")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
