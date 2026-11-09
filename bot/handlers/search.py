"""
search.py файл в котором лежат хендлеры для обработки апдейтов
"""
import asyncio

from bot.search_service.general_search import general_search
from bot.formatted_search import formatted_search_result

from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

# @dp.message()
# async def any_message(message: Message,):
#     await message.answer("Hello world")

@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    await message.answer("Добро пожаловать!")

# @router.message(Command("search"))
# async def cmd_start(message: Message) -> None:
#     await message.answer("Введите текст поиска:")

@router.message(F.text)
async def accept_search_text(message: Message, semaphore: asyncio.Semaphore):
        results, broken_providers = await general_search(message.text, semaphore)
        formatter = formatted_search_result(results, broken_providers)
        await message.answer(formatter)