# Database — public schema

## Implemented
- leads: company identity, INN, source evidence, status, qualification flags, score, permission evidence.
- lead_events: timestamped audit of state changes.
- lead_requirements: one status/value/evidence record per field.
- ownership_checks: reviewer, decision, timestamp, optional note.

## Planned
- companies, contacts, lead_sources, conversations, messages, documents, technical_specifications, configuration_items, inventory_snapshots, outreach_approvals, consent_records, handoff_events, manager_users.
- Relations: company 1:N leads; lead 1:N conversations/documents/ownership checks; technical specification 1:N configuration items.

Use Alembic migrations, unique constraints for INN and (lead_id, requirement field), RBAC, encryption, retention/deletion rules and private storage before production.
