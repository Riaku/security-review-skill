---
categories: [observability]
domains: [infrastructure]
---

# Verify The Alert Channel

**MUST** monitor the delivery path of security alerts and keep it outside the control of the component being monitored.

**Why:** A guardrail that fires into a broken or suppressible channel is indistinguishable from one that never fires, and the gap appears only during the incident.

**Detect:** command schedule a synthetic alert (`amtool alert add`, Alertmanager test alert) with an expected-receipt check and an alert when receipt is missing.

**References:** Agentic AI Top 10: AAI012 Checker-out-of-the-Loop, https://github.com/precize/Agentic-AI-Top10-Vulnerability
