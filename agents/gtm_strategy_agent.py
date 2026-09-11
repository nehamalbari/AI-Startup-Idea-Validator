import json

from deepagents import create_deep_agent

from tools.web_search import search_web

from app.config import llm


with open("prompts/gtm_agent.md", "r") as file:
    system_prompt = file.read()


gtm_agent = create_deep_agent(
    model = llm,
    tools=[search_web],
    system_prompt=system_prompt
)


def run_gtm_agent(mvp_agent_output):

    response = gtm_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": json.dumps(
                        mvp_agent_output,
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