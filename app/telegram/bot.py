"""Inbound-only Telegram bot for the public prototype.

No unsolicited messages, no LLM, no promises of price/availability.
The bot can run independently of the API for early smoke tests.
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from app.core.config import get_settings
from app.leads.gaps import QUESTIONS

router = Router()
# Prototype in-memory sessions. Replace with database-backed sessions before production.
sessions: dict[int, dict] = {}

@router.message(CommandStart())
async def start(message: Message) -> None:
    if message.chat.type != "private" or message.from_user is None:
        return
    sessions[message.from_user.id] = {"answers": {}, "step": 0}
    await message.answer(
        "Здравствуйте! Я AI-ассистент по подбору серверного оборудования. "
        "Помогу собрать технические требования и передать запрос менеджеру. "
        "Не отправляйте конфиденциальные данные или документы на этапе тестирования.\n\n"
        + QUESTIONS[0][1]
    )

@router.message(Command("status"))
async def status(message: Message) -> None:
    await message.answer("Тестовый режим: консультация без доступа к ценам, складу и CRM.")

@router.message(F.text)
async def collect(message: Message) -> None:
    if message.chat.type != "private" or message.from_user is None:
        return
    user_id = message.from_user.id
    state = sessions.get(user_id)
    if state is None:
        await message.answer("Чтобы начать консультацию, отправьте /start.")
        return
    text = (message.text or "").strip()
    if not text:
        return
    if len(text) > 1000:
        await message.answer("Пожалуйста, сократите ответ до 1000 символов.")
        return
    index = state["step"]
    if index >= len(QUESTIONS):
        await message.answer("Опрос завершён. Для повторного запуска отправьте /start.")
        return
    field, _ = QUESTIONS[index]
    if text.lower() in {"не знаю", "неизвестно", "затрудняюсь ответить"}:
        state["answers"][field] = {"status": "UNKNOWN", "value": None}
    else:
        state["answers"][field] = {"status": "CONFIRMED", "value": text}
    state["step"] += 1
    if state["step"] < len(QUESTIONS):
        await message.answer(QUESTIONS[state["step"]][1])
    else:
        lines = []
        for key, answer in state["answers"].items():
            lines.append(f"{key}: {answer['value'] or 'Клиент не знает'}")
        summary = "\n".join(lines)
        await message.answer(
            "Спасибо! Это предварительный опрос, а не зарегистрированная заявка. "
            "Данные пока хранятся только в памяти процесса.\n\n"
            + summary[:3200]
            + "\n\nМенеджеру ничего не отправлено: передача заявок появится после проверки закрепления компании."
        )

async def main() -> None:
    settings = get_settings()
    if not settings.telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN must be set in a private environment")
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=settings.telegram_bot_token)
    dp = Dispatcher()
    dp.include_router(router)
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
