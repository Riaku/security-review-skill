# payments-fraud — full checklist (11 items)

Payment flows, fraud, and money-movement safety.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/payments-fraud.md](../categories/payments-fraud.md) · Index: [SKILL.md](../SKILL.md)

# 3D Secure / SCA

**MUST** trigger 3DS2 challenge flows for high-risk transactions and honor the issuer's authentication result before capturing funds.

**Why:** Skipping SCA shifts liability onto the merchant and exposes EU/UK cards to fraudulent chargebacks under PSD2 rules.

**Detect:** grep for `three_d_secure`, `sca_required`, `exemption`, `ds.transstatus` in payment service code and gateway config.

**References:** PSD2 Article 97, EMV 3-D Secure 2.x (EMVCo), CWE-287, Stripe 3DS2 docs

# Chargebacks

**SHOULD** implement fraud detection and transaction verification to keep chargeback ratios below card brand monitoring thresholds.

**Why:** Excessive chargebacks trigger card brand fines, higher processing rates, or termination of merchant privileges.

**Detect:** grep for missing 3D Secure, AVS, velocity checks in payment flows; check `chargeback_rate`, `fraud_score`, `three_ds` config absent.

**References:** Visa VDMP, Mastercard ECP

# Dual Approval Irreversible

**MUST** require two independent approvers for high-value, irreversible actions such as large transfers, contract approvals, or safety overrides.

**Why:** A single actor who can both initiate and release an irreversible action is indistinguishable from an attacker holding that account.

**Detect:** trace the approval workflow and confirm no single identity can complete both the request and the release step.

**References:** OWASP ASVS v5.0 V2, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x11-V2-Validation-and-Business-Logic.md, NIST SP 800-53 AC-5

# Structural Invariants Against Organized Abuse

**SHOULD** detect organized abuse through structural invariants — concentrated cash-out, shared infrastructure, synchronized timing — rather than tightening per-account thresholds.

**Why:** An attacker spread across many accounts keeps each below any fixed threshold; only the structure their economics force stays visible.

**Detect:** judgment: the fraud ruleset — whether any rule keys on cross-account structure rather than a per-entity score

**References:** Fraudster's Trilemma, https://arxiv.org/abs/2605.07383

# Idempotency (idempotency keys)

**MUST** accept a client-supplied idempotency key on non-idempotent operations and deduplicate replays before executing side effects.

**Why:** A retried charge or webhook without deduplication bills the customer twice and corrupts state no rollback cleanly undoes; retried requests, network timeouts, and scripted replays trigger refund cascades that erode customer trust.

**Detect:** Check POST endpoints for `Idempotency-Key` handling, `idempotency_key` unique constraint, dedupe cache; grep payment API routes and migration files for `dedupe`.

**References:** Stripe Idempotent Requests, draft-ietf-httpapi-idempotency-key-header, CWE-837, AWS REL11-BP08

# Ledger Invariant Checks

**MUST** enforce ledger invariants continuously: sum of debits equals sum of credits, no negative balances where prohibited, every money movement has a counter-entry.

**Why:** Silent ledger drift (rounding, partial writes, bugs) compounds into real financial loss; systems without invariant checks discover errors at reconciliation time — too late to cheaply fix.

**Detect:** check for invariant assertions in the ledger layer (double-entry enforcement, balance checks in transactions), scheduled integrity queries, and alarm (not just log) on violation.

**References:** Double-entry bookkeeping in software (Martin Fowler), Stripe financial-modeling talks

# Payment Webhook Reconciliation

**SHOULD NOT** treat webhook payloads as authoritative until the signature is verified and the event is matched against a ledger entry.

**Why:** Unsigned or unreconciled webhooks let attackers forge payment confirmations and create phantom orders at zero cost.

**Detect:** check for `webhook_secret`, `stripe-signature`, `HMAC verify`, idempotency keys in webhook handler config and DB schema.

**References:** CWE-347, Stripe webhook signing guide

# PCI DSS as Audit Regime (SAQ, CDE scoping)

**MUST** scope the cardholder data environment accurately and complete the correct SAQ type (or a QSA-led ROC) for the actual card data flow, not the desired one.

**Why:** Under-scoped CDEs are the most common PCI failure: one stray database storing PANs drags the whole network into breach liability.

**Detect:** grep for "PAN", "cardholder", "CDE", "SAQ-" in configs; card data in logs, unsegmented networks, SAQ type mismatched to flow.

**References:** PCI DSS v4.0.1, SAQ A, A-EP, B, B-IP, C, C-VT, D, PCI SSC scoping guidance

# Per-Message Signing

**MUST** sign individual messages in multi-hop high-value transactions so integrity survives every intermediary, not just each transport leg.

**Why:** Transport encryption ends at each hop, so a compromised or curious intermediary can alter a payment instruction that every leg delivered intact.

**Detect:** read the payment or approval flow and check whether the instruction carries a signature the final party verifies, or only hop-by-hop TLS.

**References:** OWASP ASVS v5.0 V4, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x13-V4-API-and-Web-Service.md, NIST SP 800-53 SC-8

# Reconciliation Runbook

**SHOULD** maintain a tested reconciliation process between internal records and external sources (PSP settlement files, bank statements, partner reports) with discrepancy handling.

**Why:** Money systems disagree with their counterparties routinely; without a reconciliation runbook, every mismatch becomes a fire-drill, and real losses hide in the "we'll check later" pile.

**Detect:** look for reconciliation jobs comparing internal ledger vs PSP/bank files with tolerance thresholds; check discrepancy queue with owner and SLA; verify runbook covers partial settlements and currency mismatches.

**References:** Stripe reconciliation guidance, PCI DSS 4.0 Req 10 (logging and monitoring), payments-engineering practice guides

# Time-Bound Price Quotes

**MUST** bind prices and quotes to a short validity window and revalidate them server-side at redemption, never at display time.

**Why:** Anyone who can hold a request can freeze the terms it carries, then submit it when the market or the promotion has moved in their favour.

**Detect:** grep order and checkout handlers for `price`, `amount`, or `discount` read from the request body, and for quote records with no `expires_at`.

**References:** OWASP WSTG Testing for Payment Functionality, https://github.com/OWASP/wstg/blob/master/document/4-Web_Application_Security_Testing/10-Business_Logic/10-Payment_Functionality.md

