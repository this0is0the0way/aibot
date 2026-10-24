"""
Провайдер GitHub часть программы, которая полностью отвечайет за работу с API GitHub
"""
import httpx

async def search_github(query:str):
    async with httpx.AsyncClient() as client:
        headers = {"Accept": "application/vnd.github.v3+json",
                   "User-Agent": "StudyBotTg/0.1 (studybot@gmail.com) generic-library/0.0"}

        params = {"q": query,
                  "per_page": 3,
                  }
                                        #ednpoint
        response = await client.get("https://api.github.com/search/repositories", headers=headers, params=params)

        data = response.json()

        try:
            search_result = data["items"]
        except KeyError:
            search_result = []

        all_results = []

        for item in search_result:
            title = item["name"]
            description = item["description"]
            stars = item["stargazers_count"]
            language = item["language"]
            url = item["html_url"]
            dict_result = {"title": title,
                           "description": description,
                           "url": url,
                           "source": "GitHub",
                           "stars": stars,
                           "language": language,
                       }
            all_results.append(dict_result)
    return all_results
