"""
__main__.py отвечает за запуск пакета, можно запустить проект так python -m bot
__main__.py -специальное имя файла, которое понимает Python
"""
import asyncio
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from bot.handlers.search import router

load_dotenv()

dp = Dispatcher()
#подключение роутеров из файла, где лежат сами хендлеры. Диспетчер - Роутер - Хендлер
dp.include_router(router)

async def main():
    token = getenv("BOT_TOKEN")
    if not token:
        error = "Bot token not found"
        raise ValueError(error)
    bot = Bot(token=token)

    print("Starting bot...")
    try:
        await dp.start_polling(bot)
    finally:
        print("Stopping bot...")

if __name__ == '__main__':
    asyncio.run(main())