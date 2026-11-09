import asyncio
import logging

from aiogram import Bot, Dispatcher

from src.config import config
from src.handlers import router


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s ",
    )
    config.validate()

    bot = Bot(config.tg_token)
    dp = Dispatcher()
    dp.include_router(router)

    logging.info("Bot started, model: %s", config.llm_model)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
