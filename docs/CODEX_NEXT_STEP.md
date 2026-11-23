# Next Codex task — F01

1. Install project and run pytest.
2. Introduce Alembic migrations for all existing models; avoid runtime create_all outside test mode.
3. Add DB constraints and indexes, handle concurrent duplicate INN inserts gracefully.
4. Ensure ownership review cannot be forged by a buyer; introduce manager identity binding.
5. Add tests for INN changes invalidating ownership, handoff blocking, and field-state transitions.
6. Run ruff and pytest; report failures, changes and migration commands.
7. Do not enable outbound outreach or commit any credentials.

After F01, start F02: aiogram Telegram bot @ServermallSalesAI_bot with /start and private manager notifications. Token must be configured via environment, never Git.
