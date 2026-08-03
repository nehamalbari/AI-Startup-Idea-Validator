from langchain_core.tools import tool
from ddgs import DDGS


@tool
def search_web(query: str, max_results: int = 3) -> str:
    """Search the web for existing solutions, MVP patterns, and domain pain points."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            if not results:
                return f"No search results found for: '{query}'."

            snippets = []
            for r in results:
                title = r.get("title", "No Title")
                body = r.get("body", "No Snippet")
                snippets.append(f"Title: {title}\nSnippet: {body}")

            return "\n\n".join(snippets)

    except Exception as e:
        return (
            f"[Search Warning]: Web search encountered a temporary connection issue ({str(e)}). "
            f"Proceeding with core reasoning for query: '{query}'."
        )