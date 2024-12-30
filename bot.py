import asyncio
import logging

from aiogram.types import Message, CallbackQuery, ContentType

from core import dp, bot

from database import db
from handlers import user_handlers, admin_handlers
from states import UserState


logging.basicConfig(level=logging.INFO)


async def delete_message(message: Message):
    try:
        await message.delete()
    except Exception as e:
        print(f"Ошибка при удалении сообщения: {e}")


async def main() -> None:
    await db.initialize()

    dp.include_router(user_handlers.router)
    # dp.include_router(admin_handlers.router)

    await bot.delete_webhook(drop_pending_updates=False)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
