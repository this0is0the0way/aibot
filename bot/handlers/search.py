"""
search.py файл в котором лежат хедлеры для обработки апдейтов
"""
from bot.search_service.general_search import general_search
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
async def accept_search_text(message: Message):
    results, broken_providers = await general_search(message.text)
    if results == []:
        await message.answer("Ошибка в получении результатов от внешнего источника")
    else:
        text_msg = f"Найдено результатов: {len(results)}\n\n"
        for result in results:
            title = result["title"]
            description = result["description"]
            url = result["url"]
            source = result["source"]
            if source == "GitHub":
                stars = result["stars"]
                language = result["language"]
                if language is None:
                    language = "Язык не указан"
                text_msg += (f"{source}: {title}\n"
                             f"{description}\n"
                             f"{language}\n"
                             f"{stars}\n"
                             f"{url}\n\n")
            elif source == "StackOverFlow":
                answer_count = result["answer_count"]
                score = result["score"]
                accepted_answer = result["accepted_answer"]
                if accepted_answer is True:
                    accepted_answer = "Есть ответ на вопрос"
                else:
                    accepted_answer = "Ответа на вопрос нету"
                text_msg += (f"{source}: {title}\n"
                             f"{description}\n"
                             f"{answer_count}\n"
                             f"{score}\n"
                             f"{accepted_answer}\n\n")
            else:
                text_msg += (f"{source}: {title}\n"
                     f"{description}\n"
                     f"{url}\n\n")
        if broken_providers:
            text_msg += f"Недоступные источники:\n"
            for provider in broken_providers:
                text_msg += f"{provider}\n"

        await message.answer(text_msg)