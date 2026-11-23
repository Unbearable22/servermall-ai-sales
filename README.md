# Servermall AI Sales 100 — public prototype v0.2

B2B lead-qualification and technical presales foundation for server procurement. This repository contains **only public-safe code and generalized documentation**.

## Current status
Implemented: FastAPI REST endpoints, SQLAlchemy lead models, qualification scoring, INN checksum validation, requirement gap analysis, manual ownership checks, handoff preview, and basic tests.

**Not yet implemented:** Telegram bot integration, LLM, document intake, live warehouse access, CRM integration, automated company discovery or outreach.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env
# Replace ADMIN_API_KEY with a random strong value in .env
uvicorn app.main:app --reload
pytest -q
```
Windows: activate with `.venv\\Scripts\\activate`, copy the example environment file manually.

API: http://127.0.0.1:8000/docs

## Security
- Never commit real customer data, warehouse exports, prices, ownership mappings, internal policies, bot tokens or API keys.
- No outbound messages are implemented or enabled.
- Prototype uses `create_all`; add Alembic migrations, RBAC, encryption and privacy review before production.
- Company ownership must be manually checked before sales handoff.

See `docs/CODEX_NEXT_STEP.md` and `docs/CODEX_TASKS.md`.
