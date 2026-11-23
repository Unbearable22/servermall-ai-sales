# Architecture

FastAPI API → PostgreSQL (SQLite only for development). Future services: aiogram Telegram adapter, document intake, retrieval-based Dell knowledge, inventory adapter, lead-source adapters, LLM orchestration, human approvals, analytics. Long-running jobs via queue worker.

## Trust boundaries
External documents and customer messages are untrusted inputs, not instructions. Keep secrets in runtime environment, never Git. Warehouse exports, customer ownership records and conversations are private and must not enter public repository. Manager-facing actions require authentication and audit logs. Outbound messages disabled by default.

## Development order
1. Database migrations and explicit data constraints.
2. Telegram inbound bot and manager allowlist.
3. Document intake with size/type limits and malware scanning.
4. LLM question selection grounded in structured requirements.
5. Knowledge base with source citations and inventory validation.
6. Permissioned lead discovery, review and pilot analytics.
