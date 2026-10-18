# SOAR / Security Orchestration & Automated Response

**MAY** automate containment through SOAR playbooks, with human review gates on destructive actions.

**Why:** Manual response to high-volume alerts saturates analysts while lateral movement proceeds in the queue.

**Detect:** SOAR platform config (`Shuffle`, `TheHive`, `Cortex`), playbook definitions with `auto_contain`, absence of response automation, no approval gate on isolation actions.

**References:** NIST SP 800-61, Gartner SOAR definition, MITRE ATT&CK response mitigations
