"""
Форматирование результатов поиска и предоставлени их хендлеру в для передачи пользователю
"""
def formatted_search_result(results, broken_providers):
    if results:
        text_msg = f"Найдено результатов: {len(results)}\n\n"
        for result in results:
            title = result.title
            description = result.description
            url = result.url
            source = result.source
            if source == "GitHub":
                stars = result.stars
                language = result.language
                if language is None:
                    language = "Язык не указан"
                text_msg += (f"{source}: {title}\n"
                             f"{description}\n"
                             f"Язык программирования: {language}\n"
                             f"Звезды: {stars}\n"
                             f"{url}\n\n")
            elif source == "StackOverFlow":
                answer_count = result.answer_count
                score = result.score
                accepted_answer = result.accepted_answer
                if accepted_answer is True:
                    accepted_answer = "Есть ответ на вопрос"
                else:
                    accepted_answer = "Ответа на вопрос нету"
                text_msg += (f"{source}: {title}\n"
                             f"{url}\n"
                             f"Количество ответов: {answer_count}\n"
                             f"Рейтинг: {score}\n"
                             f"{accepted_answer}\n\n")
            else:
                text_msg += (f"{source}: {title}\n"
                             f"{description}\n"
                             f"{url}\n\n")
    else:
        text_msg = "Ничего не найдено.\n"

    if broken_providers:
        text_msg += "Недоступные источники:\n"
        for provider in broken_providers:
            text_msg += f"{provider}\n"

    return text_msg
