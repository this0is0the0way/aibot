"""
Провайдер StackOverFlow часть программы, которая полностью отвечайет за работу с API StackOverFlow
"""
import httpx

from bot.models.search_result import StackOverFlowResult

async def search_stack_ov_fl(query:str):
    async with httpx.AsyncClient() as client:
        headers = {"User-Agent": "StudyBotTg/0.1 (studybot@gmail.com) generic-library/0.0"}

        params = {"q": query,
                  "pagesize": 3,
                  "site": "stackoverflow"}

        response = await client.get("https://api.stackexchange.com/2.3/search/advanced", params=params, headers=headers)

        if response.status_code != 200:
            raise Exception(f"StackOverFlow API: HTTP {response.status_code}")

        data = response.json()

        try:
            search_result = data["items"]
        except KeyError:
            search_result = []

        all_results = []

        for item in search_result:
            title = item["title"]
            url = item["link"]
            answer_count = item["answer_count"]
            score = item["score"]
            accepted_answer = item.get("accepted_answer_id")

            if accepted_answer is None:
                accepted_answer = False
            else:
                accepted_answer = True

            result = StackOverFlowResult(title=title, url=url, description=None, source="StackOverFlow",
                                         answer_count=answer_count, score=score, accepted_answer=accepted_answer)
            all_results.append(result)
    return all_results
