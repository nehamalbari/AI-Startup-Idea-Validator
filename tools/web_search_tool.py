from ddgs import DDGS
from langchain_core.tools import tool


@tool
def search_web(query: str) -> str:
    """
    Search the web using DuckDuckGo.
    Returns the search results as formatted text.
    """

    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))

    text = ""

    for r in results:
        text += f"""
Title: {r.get("title")}
Body: {r.get("body")}
URL: {r.get("href")}

"""

    return text