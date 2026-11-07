import requests
from langchain_core.tools import tool
from config import SERPER_API_KEY

@tool
def google_search(query: str) -> dict:
    """Search Google for current information using the Serper API.
    Args:
        query: The search query to look up on Google.
    """
    url = "https://google.serper.dev/search"

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "q": query,
        "num": 5
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    results = []

    for item in data.get("organic", []):
        result = {
            "title": item.get("title", ""),
            "link": item.get("link", ""),
            "snippet": item.get("snippet", "")
        }

        results.append(result)

    return {
        "query": query,
        "results": results
    }
