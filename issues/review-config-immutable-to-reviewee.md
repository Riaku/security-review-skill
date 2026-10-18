# Review-Config Immutable to the Reviewee

**MUST** read review-automation config from the base branch (or otherwise protect it) so a PR cannot change how it is reviewed, and place CODEOWNERS on all review config.

**Why:** Cursor reads bugbot.yaml from the base branch specifically "so a PR cannot change how Bugbot reviews itself" — the general principle: review controls must not be attacker-controlled by the code under review.

**Detect:** review-config files (bot configs, thresholds, CODEOWNERS for review paths) read from PR head instead of base; missing CODEOWNERS on review automation config.

**References:** Cursor Bugbot base-branch config pattern, GitHub "requester cannot approve own agent's PR" rule
