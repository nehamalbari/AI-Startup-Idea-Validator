from deepagents import create_deep_agent
from app.config import llm
from tools.web_search_tool import search_web
from state.schema import MarketAnalysisResult
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
    market_analysis_prompt = file.read()

market_analysis_agent = create_deep_agent(
    model=llm,
    system_prompt=market_analysis_prompt,
    tools=[search_web],
    response_format=MarketAnalysisResult
)


def run_market_analysis(idea: str, industry: str, location: str) -> MarketAnalysisResult:
    """
    Run the market analysis agent for a given startup idea, industry,
    and target location. Returns a structured MarketAnalysisResult.
    """
    user_message = f"""
Startup Idea: {idea}
Industry: {industry}
Target Location: {location}

Research this market using web search, then provide a complete market
analysis covering TAM, SAM, SOM, growth rate, market maturity, key
customer segments, and key trends.
"""

    result = market_analysis_agent.invoke({
        "messages": [
            {"role": "user", "content": user_message}
        ]
    })

    structured = result.get("structured_response")
    if structured is None:
        raise ValueError(f"Agent did not return a structured response. Raw result: {result}")

    return structured