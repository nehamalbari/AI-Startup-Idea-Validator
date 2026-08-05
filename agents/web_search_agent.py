import json

from deepagents import create_deep_agent

from tools.web_search import search_web
from app.config import llm


with open("prompts/web_search_agent.md", "r") as file:
    system_prompt = file.read()


web_search_agent = create_deep_agent(
    model=llm,
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


    if isinstance(content, list):
        extracted_text = ""

        for item in content:
            if isinstance(item, dict) and "text" in item:
                extracted_text += item["text"]

        content = extracted_text

    content = content.strip()

    if content.startswith("```json"):
        content = content.replace("```json", "", 1)

    if content.endswith("```"):
        content = content[:-3]

    content = content.strip()

    

    return json.loads(content)