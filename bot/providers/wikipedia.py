"""
Провайдер Wikipedia часть программы, которая полностью отвечайет за работу с API Wikipedia
"""
import httpx
import html
import re

from bot.models.search_result import SearchResult

def clean_snippet(text:str) -> str:
    without_tags = re.sub(r'<[^>]+>', '', text)
    clean_text = html.unescape(without_tags)
    return clean_text

#функция провайдер, отправка запроска к Wikipedia
async def search_wiki(query:str):
    async with httpx.AsyncClient() as client:

        headers = {"User-Agent": "StudyBotTg/0.1 (studybot@gmail.com) generic-library/0.0"}

        params = {"action": "query",
                  "format": "json",
                  "list": "search",
                  "srsearch": query}

        response = await client.get("https://en.wikipedia.org/w/api.php",params=params, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Wikipedia API: HTTP {response.status_code}")

        data = response.json()

        try:
            search_result = data["query"]["search"]
        except KeyError:
            search_result = []

        all_results = []

        for result in search_result:
            title = result["title"]
            snippet = result["snippet"]
            page_id = result["pageid"]
            clean_text = clean_snippet(snippet)
            url = f"https://en.wikipedia.org/wiki/?curid={str(page_id)}"

            result = SearchResult(title=title, description=clean_text, url=url, source="Wikipedia")
            all_results.append(result)

            if len(all_results) == 3:
                break
    return all_results