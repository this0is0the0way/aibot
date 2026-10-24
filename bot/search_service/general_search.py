"""
general_search.py файл в котором лежит функция запуска поискогово процесса по всем источникам (провайдерам)
"""
import asyncio

import requests
from bot.providers.wikipedia import search_wiki
from bot.providers.github import search_github
from bot.providers.stack_over_flow import search_stack_ov_fl

#query = message.text

async def general_search(query: str):
        sources = {"Wikipedia": asyncio.wait_for(search_wiki(query), timeout=5),
                   "GitHub": asyncio.wait_for(search_github(query), timeout=5),
                   "StackOverFlow": asyncio.wait_for(search_stack_ov_fl(query),timeout=5),
                   }

        result = await asyncio.gather(*(sources.values()),
                                        return_exceptions=True)
        results = []
        broken_providers = []
        for source, element in zip(sources.keys(), result):
                if isinstance(element, Exception):
                    broken_providers.append(source)
                else:
                        results.extend(element)
        return results, broken_providers


