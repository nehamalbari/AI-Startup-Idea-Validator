from tools.web_search_tool import search_web
from tools.gemini_tool import ask_gemini


def web_search_agent(startup_idea):

    queries = [
        f"{startup_idea} market trends",
        f"{startup_idea} competitors",
        f"{startup_idea} customer pain points",
        f"{startup_idea} latest startup news"
    ]

    search_text = ""

    print("\nSearching the Web...\n")

    for query in queries:

        results = search_web(query)

        for result in results:

            search_text += f"""
Title: {result.get('title')}
Body: {result.get('body')}
URL: {result.get('href')}

"""

    prompt = f"""
You are an AI Web Search Agent for a Startup Idea Validator.

Analyze the search results and return ONLY the important information.

Return:

1. Market Trends
   - Maximum 3 bullet points

2. Top Competitors
   - Maximum 5 competitors
   - One-line description each

3. Customer Pain Points
   - Maximum 3 bullet points

4. Latest News
   - Maximum 3 bullet points

Rules:
- Keep response under 300 words.
- Use short bullet points.
- No long paragraphs.
- No unnecessary explanation.
- Be concise and professional.

Search Results:

{search_text}
"""

    report = ask_gemini(prompt)

    return report