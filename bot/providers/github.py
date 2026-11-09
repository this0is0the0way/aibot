"""
Провайдер GitHub часть программы, которая полностью отвечайет за работу с API GitHub
"""
import httpx

from bot.models.search_result import GitHubResult

async def search_github(query:str):
    async with httpx.AsyncClient() as client:
        headers = {"Accept": "application/vnd.github.v3+json",
                   "User-Agent": "StudyBotTg/0.1 (studybot@gmail.com) generic-library/0.0"}

        params = {"q": query,
                  "per_page": 3,
                  }
                                        #ednpoint
        response = await client.get("https://api.github.com/search/repositories", headers=headers, params=params)

        if response.status_code != 200:
            raise Exception(f"GitHub API: HTTP {response.status_code}")

        data = response.json()

        try:
            search_result = data["items"]
        except KeyError:
            search_result = []

        all_results = []

        for item in search_result:
            title = item["full_name"]
            description = item["description"]
            stars = item["stargazers_count"]
            language = item["language"]
            url = item["html_url"]

            result = GitHubResult(title=title, description=description, url=url, source="GitHub",
                                  stars=stars, language=language)
            all_results.append(result)
    return all_results
