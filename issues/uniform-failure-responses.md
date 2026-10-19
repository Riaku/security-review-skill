---
categories: [authentication]
domains: [backend]
---

# Uniform Failure Responses

**MUST** complete the expensive security check before returning a failure, so that rejection timing does not reveal whether the account, token, or key exists.

**Why:** A fast 'not found' and a slow 'wrong secret' are the same oracle in different units; attackers measure microseconds, not messages.

**Detect:** grep verification handlers for an early return before the hash comparison or the key lookup (unknown user, malformed token, missing key), and for per-cause error strings; the not-found path that skips the expensive check is the finding.

**References:** Lucky Thirteen timing analysis, https://www.imperialviolet.org/2013/02/04/luckythirteen.html, CWE-203 Observable Discrepancy
