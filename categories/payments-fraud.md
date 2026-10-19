# payments-fraud

Payment flows, fraud, and money-movement safety.

## What this category covers

This category covers the correctness and integrity of money movement and the fraud, authentication, and settlement controls that ride on it. Items span payment authentication and chargeback management, retry deduplication for non-idempotent money operations, ledger invariants, and reconciliation between internal records and external settlement sources. A reviewer should expect to see charge, refund, and transfer endpoints, webhook handlers, a ledger or double-entry layer, and reconciliation jobs against PSP or bank files. The card-data scope of PCI DSS is represented here alongside the payment flows it governs.

- Payment authentication and fraud controls — 3DS and SCA challenge flows, AVS and velocity checks, and chargeback-ratio management.
- Retry deduplication and replay safety — client-supplied dedupe keys on non-idempotent money operations, checked before side effects run.
- Ledger integrity — double-entry invariants, non-negative balances, and a counter-entry for every money movement.
- Webhook and settlement reconciliation — verifying webhook signatures and matching events to ledger entries, plus scheduled reconciliation against PSP settlement files and bank statements.
- Card-data scope — PCI DSS SAQ and CDE scoping for the card-data flow that actually exists.

## What it does not cover

- [regulatory-frameworks](../categories/regulatory-frameworks.md) — PCI DSS attestation, NYDFS 23 NYCRR 500, DORA, and SEC disclosure regimes belong there; the card-data flow and payment mechanics are scoped here.
- [database](../categories/database.md) — transactions, unique constraints, and ledger storage mechanics belong there; the payment invariants those mechanics must uphold are scoped here.
- [messaging-async](../categories/messaging-async.md) — queue semantics, dead-letter queues, and general webhook replay protection belong there; confirming a payment webhook against the ledger is scoped here.
- [third-party-integrations](../categories/third-party-integrations.md) — OAuth scope minimization and processor or SaaS credential sprawl belong there; trusting a processor's payment confirmation is scoped here.

## What a finding here looks like

- A charge or webhook endpoint with no dedupe key and no dedupe store, so a retried request bills the customer twice.
- A webhook handler that trusts its payload before verifying the signature and matching the event to a ledger entry.
- A ledger write path with no assertion that debits equal credits or that each movement has a counter-entry.
- 3DS or SCA skipped on a high-risk transaction, or the issuer's authentication result ignored before capture.
- Reconciliation comparing internal records to PSP settlement files with no owner or SLA on unresolved discrepancies.
