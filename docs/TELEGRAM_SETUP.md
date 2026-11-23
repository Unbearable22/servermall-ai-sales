# Telegram smoke test (public-safe)

Bot: @ServermallSalesAI_bot

1. Install dependencies: `pip install -e '.[dev]'`.
2. Set `TELEGRAM_BOT_TOKEN` as a private environment variable. Never paste it into a chat or commit it to Git.
3. Run `python -m app.telegram.bot` in a persistent terminal or server.
4. Open the bot, send `/start`, answer questions; `не знаю` records UNKNOWN.
5. Send `/status` to verify test mode.

Limitations: only in-memory sessions; no document uploads, no manager notifications, no INN routing, no database persistence, no LLM, no actual sales outreach. Do not send real client data during this phase. A Telegram bot cannot initiate private conversations with arbitrary users.

Next: persistent conversations, role-bound manager identity, safe file intake and ownership check before handoff.
