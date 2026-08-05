import json

from deepagents import create_deep_agent

from tools.web_search import search_web


with open("prompts/market_analysis_agent.md", "r") as file:
    system_prompt = file.read()


market_agent = create_deep_agent(
    tools=[search_web],
    system_prompt=system_prompt,
)


def run_market_agent(web_search_output):

    response = market_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": json.dumps(
                        web_search_output,
                        indent=4
                    ),
                }
            ]
        }
    )

    content = response["messages"][-1].content

    if content.startswith("```json"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

    return json.loads(content)