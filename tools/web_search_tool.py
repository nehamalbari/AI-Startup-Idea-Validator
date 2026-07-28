from ddgs import DDGS


def search_web(query: str, max_results: int = 5):
    """
    Search the web using DuckDuckGo.

    Args:
        query (str): Search query.
        max_results (int): Number of results.

    Returns:
        list: Search results.
    """
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=max_results))

    return results