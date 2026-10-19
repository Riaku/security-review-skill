---
categories: [payments-fraud]
domains: [backend]
---

# Time-Bound Price Quotes

**MUST** bind prices and quotes to a short validity window and revalidate them server-side at redemption, never at display time.

**Why:** Anyone who can hold a request can freeze the terms it carries, then submit it when the market or the promotion has moved in their favour.

**Detect:** grep order and checkout handlers for `price`, `amount`, or `discount` read from the request body, and for quote records with no `expires_at`.

**References:** OWASP WSTG Testing for Payment Functionality, https://github.com/OWASP/wstg/blob/master/document/4-Web_Application_Security_Testing/10-Business_Logic/10-Payment_Functionality.md
