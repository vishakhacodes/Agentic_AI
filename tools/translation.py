import requests


def _normalize_language(code: str):
    if not code:
        return None
    code = str(code).strip().lower()
    mapping = {
        "english": "en",
        "en": "en",
        "spanish": "es",
        "es": "es",
        "hindi": "hi",
        "hi": "hi",
        "french": "fr",
        "fr": "fr",
        "german": "de",
        "de": "de",
        "italian": "it",
        "it": "it",
        "portuguese": "pt",
        "pt": "pt",
        "arabic": "ar",
        "ar": "ar",
        "japanese": "ja",
        "ja": "ja",
        "chinese": "zh",
        "zh": "zh",
        "russian": "ru",
        "ru": "ru",
    }
    return mapping.get(code, code[:2])


def execute(arguments: dict):
    text = arguments.get("text") or arguments.get("message") or arguments.get("content")
    target_language = arguments.get("target_language") or arguments.get("to") or arguments.get("target")
    source_language = arguments.get("source_language") or arguments.get("from_lang") or arguments.get("source")

    if not text:
        return "Translation error: text is required"
    if not target_language:
        return "Translation error: target_language is required"

    try:
        source_code = _normalize_language(source_language) or "en"
        target_code = _normalize_language(target_language)
        response = requests.get(
            "https://api.mymemory.translated.net/get",
            params={"q": text, "langpair": f"{source_code}|{target_code}"},
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
        translated = payload.get("responseData", {}).get("translatedText")
        if translated:
            return translated
        return f"Translation error: {payload}"
    except Exception as exc:
        return f"Translation error: {exc}"
