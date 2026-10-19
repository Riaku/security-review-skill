# Security Policy

This repository is a corpus of review guidance, not a running service. The
security-relevant surface is small but real: the CI workflow, the two scripts in
`scripts/`, and the actions the workflow runs.

## Reporting a vulnerability

Use **GitHub private vulnerability reporting** — the *Report a vulnerability*
button under the repository's **Security** tab. It opens a private advisory only
the maintainer can see, so there is no need to email or open a public issue.

Please report privately if the problem is one of:

- code execution or permission escalation through `.github/workflows/`
  (for example an unpinned action, an over-broad `permissions:` block, or a
  script that reads attacker-controlled input from a pull request)
- a supply-chain problem in either pinned action, or a pinned SHA that no longer
  matches the version its comment claims
- something in `scripts/` that can be made to write outside the working tree
- a security claim in an item that is wrong in a way that would cause a reader to
  ship an exploitable system

## Not vulnerabilities here

- **Guidance you disagree with.** An item that is too strict, too vague, or
  duplicates another is a content issue — open a normal issue or PR. Quote the
  item slug.
- **Dead or moved reference links.** Also a normal issue; note that roughly 20
  hosts (CISA, ISO, some government portals) block datacenter IPs, so confirm a
  link is dead from a residential connection before reporting.
- **A finding about a project that used this skill.** Report it to that project.

## What to expect

Best-effort handling by a solo maintainer: an acknowledgement, then a fix or a
written explanation in the advisory thread. There is no bug bounty and no paid
programme. Please give a reasonable window before disclosing publicly; if a
report involves one of the pinned actions upstream, it may need to go to that
project first.

## Supported versions

This repository is not versioned with releases, and `main` is the only supported
branch — always report against the current `main`.
