import json
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from deepagents import create_deep_agent

from tools.web_search_tool import search_web
from state.schema import WebSearchReport

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3,
)

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

prompt_path = os.path.join(
    BASE_DIR,
    "prompts",
    "web_search_agent.md"
)

with open(prompt_path, "r", encoding="utf-8") as file:
    web_search_prompt = file.read()


web_search_agent = create_deep_agent(
    model=llm,
    system_prompt=web_search_prompt,
    tools=[search_web]
)


def run_web_search(startup_idea: str) -> WebSearchReport:

    response = web_search_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"""
Research this startup idea:

{startup_idea}

Return ONLY valid JSON.
"""
                }
            ]
        }
    )

    final_text = response["messages"][-1].content.strip()

    if final_text.startswith("```"):
        final_text = (
            final_text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

    data = json.loads(final_text)

    return WebSearchReport(**data)