---
categories: [email-security]
domains: [governance, infrastructure]
---

# Email Bounce Handling

**MUST** consume hard bounces and spam complaints programmatically and feed them into a suppression list so invalid addresses are never mailed again.

**Why:** Mailing dead addresses tanks sender reputation; Gmail and Outlook then divert the whole domain's legitimate mail to spam, and ignored abuse complaints can get the sending IP delisted for weeks.

**Detect:** Check whether SES/SendGrid bounce and complaint notifications have a live SNS consumer — a notification config with no subscriber is the classic gap. Grep for suppression checks before send, and for retry loops that requeue bounced mail.

**Bad:**
```python
for addr in mailing_list:
    send(to=addr, ...)   # bounces go nowhere; we re-send next campaign anyway
```

**Good:**
```python
if suppressed(addr):     # populated from SNS bounce/complaint consumer
    continue
send(to=addr, ...)
```

**References:** AWS SES bounce & complaint handling docs, Gmail Sender Guidelines, M3AAWG sender best practices
