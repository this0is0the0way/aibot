"""
Провайдер StackOverFlow часть программы, которая полностью отвечайет за работу с API StackOverFlow
"""
import httpx

async def search_stack_ov_fl(query:str):
    async with httpx.AsyncClient() as client:
        headers = {"User-Agent": "StudyBotTg/0.1 (studybot@gmail.com) generic-library/0.0"}

        params = {"q": query,
                  "site": "stackoverflow"}


        response = await client.get("https://api.stackexchange.com/2.3/search/advanced", params=params, headers=headers)

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

            dict_result = {"title": title,
                           "url": url,
                           "answer_count": answer_count,
                           "score": score,
                           "accepted_answer": accepted_answer,
                           "source": "StackOverFlow",
                           "description": None
                           }
            all_results.append(dict_result)
            if len(all_results) == 3:
                break
    return all_results
