from __future__ import annotations

import pytest

from nanobot.bus.queue import MessageBus
from nanobot.channels.telegram import TelegramChannel


class _User:
    id = 999
    username = "intruder"
    first_name = "Intruder"


class _Chat:
    type = "private"
    is_forum = False


class _Message:
    chat_id = 12345
    chat = _Chat()
    message_id = 1
    text = "hello"
    caption = None
    location = None
    media_group_id = None
    reply_to_message = None
    message_thread_id = None
    photo = None
    voice = None
    audio = None
    document = None
    video = None
    video_note = None
    animation = None


class _Update:
    message = _Message()
    effective_user = _User()


def test_telegram_security_defaults() -> None:
    ch = TelegramChannel({"allowFrom": ["123"]}, MessageBus())

    assert ch.config.drop_pending_updates is True
    assert ch.config.inbound_rate_limit_count == 20
    assert ch.config.inbound_rate_limit_window_s == 60.0


def test_telegram_rate_limit_blocks_excess_messages() -> None:
    ch = TelegramChannel(
        {
            "allowFrom": ["123"],
            "inboundRateLimitCount": 1,
            "inboundRateLimitWindowS": 60,
        },
        MessageBus(),
    )

    assert ch._authorize_sender("123", apply_rate_limit=True) is True
    assert ch._authorize_sender("123", apply_rate_limit=True) is False


@pytest.mark.asyncio
async def test_telegram_rejects_unauthorized_before_media_download(monkeypatch) -> None:
    ch = TelegramChannel({"allowFrom": ["123"]}, MessageBus())
    called = False

    async def fail_if_called(*_args, **_kwargs):
        nonlocal called
        called = True
        return [], []

    monkeypatch.setattr(ch, "_download_message_media", fail_if_called)

    await ch._on_message(_Update(), None)

    assert called is False
    assert ch._chat_ids == {}
