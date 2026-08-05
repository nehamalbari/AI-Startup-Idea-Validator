import json

from deepagents import create_deep_agent

from tools.web_search import search_web


with open("prompts/competitor_agent.md", "r") as file:
    system_prompt = file.read()


competitor_agent = create_deep_agent(
    tools=[search_web],
    system_prompt=system_prompt,
)


def run_competitor_agent(market_analysis_output):

    response = competitor_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": json.dumps(
                        market_analysis_output,
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