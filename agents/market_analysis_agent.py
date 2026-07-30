import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage

from tools.web_search_tool import search_web
from state.market_analysis_schema import MarketAnalysis

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. Copy .env.example to .env and add your key "
        "from https://console.groq.com"
    )

model = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=GROQ_API_KEY,
    temperature=0.3,
)

TOOLS = [search_web]
TOOLS_BY_NAME = {t.name: t for t in TOOLS}
model_with_tools = model.bind_tools(TOOLS)

SYSTEM_PROMPT = """
You are the Market Analysis Agent inside a startup validation system.

Given a startup idea, industry, and target location, research and estimate the
market opportunity SPECIFIC TO THAT LOCATION.

Use the search_web tool as many times as needed — search for market size,
growth trends, and customer segments for the given location before answering.

Once you have enough information, respond with ONLY valid JSON, no preamble,
no markdown fences, matching exactly this structure:
{
  "location": "the target location provided",
  "tam": "string with estimated $ value and 1-line reasoning",
  "sam": "string with estimated $ value and 1-line reasoning",
  "som": "string with estimated $ value and 1-line reasoning",
  "growth_rate": "string, e.g. '12% CAGR (2024-2029)'",
  "customer_segments": [{"name": "string", "description": "string"}],
  "market_maturity": "Emerging | Growing | Mature | Declining",
  "key_trends": ["string", "string"]
}

CRITICAL RULES:
- TAM must be the largest number, SAM smaller (a subset of TAM), SOM smallest (a subset of SAM)
- All figures must reflect the specified location, not the global market,
  unless the location given is "Global" or "Worldwide"
- Base estimates on real search results where possible; if data is unavailable,
  say so explicitly rather than inventing false precision
- Once you have enough search results, STOP calling tools and respond with the
  final JSON only.
"""

MAX_STEPS = 6  # safety cap so a confused model can't loop forever


def run_market_analysis(startup_idea: str, industry: str, location: str) -> MarketAnalysis:
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=(
            f"Startup idea: {startup_idea}\n"
            f"Industry: {industry}\n"
            f"Target Location: {location}\n\n"
            "Research and provide the market analysis JSON."
        )),
    ]

    final_text = None

    for _ in range(MAX_STEPS):
        ai_message = model_with_tools.invoke(messages)
        messages.append(ai_message)

        if not ai_message.tool_calls:
            final_text = ai_message.content
            break

        for tool_call in ai_message.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_fn = TOOLS_BY_NAME.get(tool_name)

            if tool_fn is None:
                tool_result = f"Error: unknown tool '{tool_name}'"
            else:
                tool_result = tool_fn.invoke(tool_args)

            messages.append(ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"],
            ))
    else:
        # Loop exhausted without a final answer — force one, no tools.
        messages.append(HumanMessage(
            content="Stop searching now. Respond with ONLY the final JSON."
        ))
        final_ai_message = model.invoke(messages)
        final_text = final_ai_message.content

    if not final_text:
        raise ValueError("Agent finished without producing any output.")

    cleaned = final_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    cleaned = cleaned.strip()

    parsed = json.loads(cleaned)

    return MarketAnalysis(**parsed)

