from deepagents import create_deep_agent
from app.config import llm
from tools.web_search import search_web
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


prompt_path = os.path.join(
    BASE_DIR,
    "prompts",
    "market_analysis_agent.md"
)


with open(prompt_path, "r", encoding="utf-8") as file:
    market_prompt = file.read()


market_agent = create_deep_agent(
    model=llm,
    system_prompt=market_prompt,
    tools=[search_web]
)