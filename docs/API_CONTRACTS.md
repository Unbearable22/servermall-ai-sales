# API contracts v0.2

All /api/v1 endpoints require X-API-Key; /health is public.

- GET /health — status and safety flags.
- POST /api/v1/leads — {company_name, inn?, source_url?, source_evidence?}; 201 or 409/422.
- GET /api/v1/leads?limit=50 — list of leads.
- GET /api/v1/leads/{id} — lead details.
- PATCH /api/v1/leads/{id}/qualification — five boolean scoring fields.
- PATCH /api/v1/leads/{id}/status — {status, reason}; invalid transitions 409.
- PUT /api/v1/leads/{id}/requirements/{field} — {status, value?, source?, evidence?}.
- GET /api/v1/leads/{id}/requirements — field values and next questions.
- PATCH /api/v1/leads/{id}/inn — {inn}; checksum validated.
- POST /api/v1/leads/{id}/ownership-review — {result, checked_by, note?}.
- GET /api/v1/leads/{id}/handoff-preview — lead summary and ownership gate.

Not implemented: Telegram webhook, file upload, inventory, CRM, messaging, LLM and autonomous prospecting.
