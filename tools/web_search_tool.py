from ddgs import DDGS
from langchain_core.tools import tool


@tool
def search_web(query: str) -> str:
    """
    Search the web using DuckDuckGo.
    Returns the top search results as formatted text.
    """

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))

        if not results:
            return "No search results found."

        text = ""

        for r in results:
            text += f"""
Title: {r.get("title", "N/A")}
Body: {r.get("body", "N/A")}
URL: {r.get("href", "N/A")}

"""

        return text

    except Exception as e:
        return f"Search failed: {str(e)}"