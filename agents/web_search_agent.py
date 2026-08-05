import json

from deepagents import create_deep_agent

from tools.web_search import search_web


with open("prompts/web_search_agent.md", "r") as file:
    system_prompt = file.read()


web_search_agent = create_deep_agent(
    tools=[search_web],
    system_prompt=system_prompt,
)


def run_web_search_agent(startup_idea: str):

    response = web_search_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"""
Startup Idea:

{startup_idea}

Search the web and return the result in JSON format.
""",
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