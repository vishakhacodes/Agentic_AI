import requests
import re
from urllib.parse import quote


SEARCH_URLS = [
    "https://r.jina.ai/http://www.bing.com/search?q={}",
    "https://r.jina.ai/http://www.duckduckgo.com/html/?q={}",
    "https://duckduckgo.com/html/?q={}",
    "https://lite.duckduckgo.com/lite/?q={}",
]


def _extract_jina_results(text: str):
    results = []
    for match in re.finditer(r"Title:\s*(.+?)\s*URL Source:\s*(https?://\S+)", text, re.I | re.S):
        title = match.group(1).strip()
        link = match.group(2).strip()
        results.append(f"- {title}: {link}")

    if results:
        return results

    if "Markdown Content:" in text:
        content = text.split("Markdown Content:", 1)[1]
        for title, link in re.findall(r"\*+\s*\[([^\]]+)\]\((https?://[^)]+)\)", content):
            results.append(f"- {title.strip()}: {link.strip()}")
        if results:
            return results

    return []


def _extract_html_results(html: str):
    results = []
    titles = re.findall(r"<a[^>]+class=\"result__a\"[^>]+href=\"([^\"]+)\"[^>]*>([^<]+)</a>", html)
    if titles:
        for link, title in titles[:5]:
            results.append(f"- {title.strip()}: {link.strip()}")
        return results

    bing_results = re.findall(r"<li class=\"b_algo\".*?<a[^>]+href=\"([^\"]+)\"[^>]*>(.*?)</a>", html, re.S)
    if bing_results:
        for link, title in bing_results[:5]:
            clean_title = re.sub(r"<[^>]+>", "", title).strip()
            results.append(f"- {clean_title}: {link.strip()}")
        return results

    generic = re.findall(r"<a[^>]+href=\"([^\"]+)\"[^>]*>([^<]+)</a>", html)
    if generic:
        for link, title in generic[:5]:
            clean_title = re.sub(r"<[^>]+>", "", title).strip()
            results.append(f"- {clean_title}: {link.strip()}")
        return results

    return []


def execute(arguments: dict):
    query = arguments.get("query") or arguments.get("search") or arguments.get("text")
    if not query:
        return "Web search error: query is required"

    encoded_query = quote(query)
    last_error = None

    for url_template in SEARCH_URLS:
        url = url_template.format(encoded_query)
        try:
            response = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            body = response.text
            if not body:
                continue

            if "Please complete the following challenge" in body:
                last_error = Exception("search provider blocked the request")
                continue

            results = _extract_jina_results(body)
            if not results:
                results = _extract_html_results(body)

            if results:
                return "\n".join(results)

            text = re.sub(r"<[^>]+>", " ", body)
            text = re.sub(r"\s+", " ", text).strip()
            if text:
                return text[:4000]
        except Exception as exc:
            last_error = exc
            continue

    return f"Web search error: {last_error}"
