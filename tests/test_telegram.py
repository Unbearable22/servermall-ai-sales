import pytest
from unittest.mock import AsyncMock
from types import SimpleNamespace
from app.telegram.bot import start, collect, sessions

@pytest.mark.asyncio
async def test_start_and_unknown_response():
    sessions.clear()
    msg = SimpleNamespace(chat=SimpleNamespace(type="private"),
                          from_user=SimpleNamespace(id=123),
                          answer=AsyncMock(), text="/start")
    await start(msg)
    assert sessions[123]["step"] == 0
    msg.text = "не знаю"
    await collect(msg)
    assert sessions[123]["answers"]["purpose"]["status"] == "UNKNOWN"
    assert sessions[123]["step"] == 1

@pytest.mark.asyncio
async def test_no_session():
    sessions.clear()
    msg = SimpleNamespace(chat=SimpleNamespace(type="private"),
                          from_user=SimpleNamespace(id=456),
                          answer=AsyncMock(), text="Нужен сервер")
    await collect(msg)
    msg.answer.assert_awaited_once()
