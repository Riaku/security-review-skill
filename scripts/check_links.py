#!/usr/bin/env python3
"""Link checker for the skill repo.

Extracts http(s) URLs from markdown files and checks they resolve.
Placeholder/example URLs are skipped by pattern (they document attack
targets, not references). Network failures are retried once; persistent
4xx/5xx are reported as broken.

Usage:
  python3 scripts/check_links.py            # check all md files
  python3 scripts/check_links.py --offline  # only validate URL syntax/placeholders
"""
import re
import sys
import pathlib
import urllib.request
import urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent

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


def fetch_ok(url: str) -> tuple[bool, str]:
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, method=method, headers=UA)
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return True, str(r.status)
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (403, 405, 501):
                continue  # try GET
            return False, str(e.code)
        except Exception as e:
            return False, type(e).__name__
    return False, "unreachable"


def main() -> int:
    offline = "--offline" in sys.argv
    files = sorted(p for p in ROOT.rglob("*.md")
                  if ".git" not in p.parts)
    urls = {}
    for f in files:
        for m in URL_RE.finditer(f.read_text(encoding="utf-8", errors="ignore")):
            u = m.group(0).rstrip(".,;:")
            urls.setdefault(u, set()).add(str(f.relative_to(ROOT)))

    real = {u: v for u, v in urls.items() if not is_placeholder(u)}
    skipped = len(urls) - len(real)
    broken = []
    if not offline:
        for u in sorted(real):
            ok, status = fetch_ok(u)
            mark = "ok " if ok else "FAIL"
            print(f"  {mark} {status:>4}  {u}")
            if not ok:
                broken.append((u, status, sorted(real[u])))
    else:
        print(f"offline mode: {len(real)} real URLs would be checked")

    print(f"\nlinks: {len(real)} checked, {skipped} placeholders skipped, "
          f"{len(broken)} broken")
    for u, status, where in broken:
        print(f"  BROKEN {status}: {u}")
        for w in where:
            print(f"    in {w}")
    return 1 if broken else 0


if __name__ == "__main__":
    raise SystemExit(main())
