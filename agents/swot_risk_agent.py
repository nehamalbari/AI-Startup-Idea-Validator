import json

from deepagents import create_deep_agent

from tools.web_search import search_web

from app.config import llm


with open("prompts/swot_risk_agent.md", "r") as file:
    system_prompt = file.read()


swot_agent = create_deep_agent(
    model = llm,
    tools = [search_web],
    system_prompt=system_prompt,
)


def run_swot_agent(competitor_analysis_output):

    response = swot_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": json.dumps(
                        competitor_analysis_output,
                        indent=4
                    ),
                }
            ]
        }
    )

    content = response["messages"][-1].content

    if isinstance(content, list):
        content = content[0]["text"]

    content = content.strip()

    if content.startswith("```json"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

    return json.loads(content)