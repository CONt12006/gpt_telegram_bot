import logging

from aiogram import F, Router
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.types import Message

from src import llm
from src.config import config
from src.history import DialogHistory

router = Router()
history = DialogHistory(config.max_history)
log = logging.getLogger(__name__)

TG_LIMIT = 4000  # Telegram hard limit is 4096 chars per message


def _allowed(msg: Message) -> bool:
    return not config.allowed_users or msg.from_user.id in config.allowed_users


@router.message(Command("start"))
async def cmd_start(msg: Message) -> None:
    await msg.answer(
        "Привет! Пиши что угодно — я передам это нейросети.\n"
        "/reset — очистить историю диалога\n"
        f"Модель: {config.llm_model}"
    )


@router.message(Command("reset"))
async def cmd_reset(msg: Message) -> None:
    history.clear(msg.from_user.id)
    await msg.answer("История очищена.")


@router.message(F.text)
async def on_text(msg: Message) -> None:
    if not _allowed(msg):
        await msg.answer("Доступ запрещён.")
        return

    user_id = msg.from_user.id
    history.add(user_id, "user", msg.text)
    await msg.bot.send_chat_action(msg.chat.id, ChatAction.TYPING)

    try:
        answer = await llm.ask(history.get(user_id))
    except Exception as e:
        log.exception("LLM request failed")
        await msg.answer(f"Ошибка API: {e}")
        return

    history.add(user_id, "assistant", answer)
    for i in range(0, len(answer), TG_LIMIT):
        await msg.answer(answer[i : i + TG_LIMIT])
