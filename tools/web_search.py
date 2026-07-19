import requests
import re
from urllib.parse import quote


def execute(arguments: dict):
    query = arguments.get("query") or arguments.get("search") or arguments.get("text")
    if not query:
        return "Web search error: query is required"

    encoded_query = quote(query)
    search_urls = [
        f"https://duckduckgo.com/html/?q={encoded_query}",
        f"https://lite.duckduckgo.com/lite/?q={encoded_query}",
    ]

    last_error = None
    for url in search_urls:
        try:
            response = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            html = response.text
            if not html:
                continue

            if "lite.duckduckgo.com" in url:
                snippets = re.findall(r"<a rel=\"nofollow\" class=\"result__a\" href=\"([^\"]+)\">([^<]+)</a>", html)
                if snippets:
                    results = []
                    for link, title in snippets[:5]:
                        results.append(f"- {title}: {link}")
                    return "\n".join(results)

            titles = re.findall(r"<a rel=\"nofollow\" class=\"result__a\" href=\"([^\"]+)\">([^<]+)</a>", html)
            if titles:
                results = []
                for link, title in titles[:5]:
                    results.append(f"- {title}: {link}")
                return "\n".join(results)

            text = re.sub(r"<[^>]+>", " ", html)
            text = re.sub(r"\s+", " ", text).strip()
            if text and "Please complete the following challenge" not in text:
                return text[:4000]

            if "Please complete the following challenge" in html:
                return (
                    f"Live web search is currently blocked by the search provider for query '{query}'. "
                    "Try again shortly or use a different search source."
                )
        except Exception as exc:
            last_error = exc

    return f"Web search error: {last_error}"
