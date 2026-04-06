# Design Decisions <!-- omit from toc -->

## Table of Contents <!-- omit from toc -->

- [Why Batch Processing](#why-batch-processing)
- [Why Gmail Labels](#why-gmail-labels)
- [Why Manual Review Step](#why-manual-review-step)
- [Why .env Configuration](#why-env-configuration)
- [Why Structured Logging](#why-structured-logging)
- [Design Focus](#design-focus)
- [## Example Run](#-example-run)
---

## Why Batch Processing

Emails are processed in batches instead of individually.

This allows:
- consistent execution
- easier tracking
- clear start and end boundaries

Each batch can be treated as a single unit of work.

---

## Why Gmail Labels

Gmail labels act as the control mechanism.

Instead of scanning the entire inbox:
- only labeled emails are processed
- processed emails are moved automatically

This keeps the workflow predictable and controlled.

---

## Why Manual Review Step

Automation is separated from sending.

Export → Review → Send

This prevents:
- accidental sends
- incorrect formatting
- incomplete data being shared

It adds a safety layer without removing automation.

---

## Why .env Configuration

All configuration is externalized.

Benefits:
- no code changes required
- safer for users
- easier environment setup
- consistent across systems

---

## Why Structured Logging

Logging is designed for readability and traceability.

Each run includes:
- batch ID
- start and end boundaries
- per-item tracking

This makes debugging fast and reliable.

The goal is simple:

"Understand what happened without guessing."

## Design Focus

This project emphasizes traceability, repeatability, and controlled automation over raw speed.

## ## Example Run

```
[RUN START][job_batch_20260403_211500]
Processed : 2
Success : 1
Failed : 1
[RUN END]
```