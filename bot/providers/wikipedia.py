"""
Провайдер Wikipedia часть программы, которая полностью отвечайет за работу с API Wikipedia
"""
#from urllib.parse import quote
import httpx
import html
import re


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
            #formatted_title = quote(title.replace(" ", "_"))
            #url = "https://en.wikipedia.org/wiki/" + formatted_title
            url = f"https://en.wikipedia.org/wiki/?curid={str(page_id)}"
            dict_result = {"title": title,
                           "description": clean_text,
                           "url": url,
                           "source": "Wikipedia",
                           }
            all_results.append(dict_result)
            if len(all_results) == 3:
                break
    return all_results