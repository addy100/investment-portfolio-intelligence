# ETL jobs

Scheduled jobs belong here. Each job must be idempotent, record its source and as-of date, and never ingest broker credentials from the repository.

`refresh.py` is intentionally a safe placeholder for Sprint 1. Sprint 2 will add a user-authorized Zerodha import adapter and transaction normalization.
