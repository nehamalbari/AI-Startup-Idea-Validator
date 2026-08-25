from ddgs import DDGS
from langchain_core.tools import tool
import time


@tool
def search_web(query: str) -> str:
    """
    Search the web using DuckDuckGo.
    Returns the search results as formatted text.
    """

    for attempt in range(3):
        try:
            with DDGS() as ddgs:
                results = list(
                    ddgs.text(
                        query,
                        max_results=5
                    )
                )

            text = ""

            for r in results:
                text += f"""
Title: {r.get("title")}
Body: {r.get("body")}
URL: {r.get("href")}

"""

            return text

        except Exception as e:
            print(
                f"[Web Search] Attempt {attempt + 1}/3 failed: {e}"
            )

            if attempt < 2:
                time.sleep(2)

    return "Web search failed after 3 attempts."