"""
Web Search Agent (Deep Agent)

Uses:
- LangChain tool calling
- Multi-step reasoning
- Pydantic output
"""

import os
import json

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    ToolMessage,
)

from tools.web_search_tool import search_web
from state.schema import WebSearchReport

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found")

model = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=GROQ_API_KEY,
    temperature=0.3,
)

TOOLS = [search_web]
TOOLS_BY_NAME = {tool.name: tool for tool in TOOLS}

model_with_tools = model.bind_tools(TOOLS)

MAX_STEPS = 5
SYSTEM_PROMPT = """
You are the Web Search Agent inside an AI Startup Validator.

Your task is to autonomously search the web and analyze the search results.

Do NOT copy webpage titles or URLs directly.

Instead:
- Read all search results.
- Identify the most important information.
- Summarize the information into concise insights.
- Combine similar information into one point.
- Ignore advertisements and duplicate results.

Return ONLY valid JSON in the following format:

{
    "market_trends": [
        "...",
        "...",
        "..."
    ],
    "customer_pain_points": [
        "...",
        "...",
        "..."
    ],
    "latest_news": [
        "...",
        "...",
        "..."
    ],
    "industry_insights": [
        "...",
        "...",
        "..."
    ]
}

Rules:
- Return ONLY valid JSON.
- Do NOT include markdown.
- Do NOT include explanations.
- Do NOT copy webpage titles.
- Do NOT copy URLs.
- Each point should be a meaningful summary (1-2 sentences maximum).
- Maximum 3 points per section.
- If multiple search results say the same thing, merge them into one insight.
- Latest news must describe recent developments, not article titles.
- Industry insights should explain the industry, not list websites.

"""


def run_web_search(startup_idea: str) -> WebSearchReport:

    messages = [

        SystemMessage(content=SYSTEM_PROMPT),

        HumanMessage(
            content=f"""
Startup Idea:

{startup_idea}

Search the web and return the JSON.
"""
        )
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

            tool = TOOLS_BY_NAME.get(tool_name)

            if tool is None:

                result = f"Unknown tool {tool_name}"

            else:

                result = tool.invoke(tool_args)
                cleaned_result = str(result)
                cleaned_result = cleaned_result.replace("\n", " ")
                cleaned_result = " ".join(cleaned_result.split())
                messages.append(
                    ToolMessage(
                        content=cleaned_result,
                        tool_call_id=tool_call["id"]
    )
)

    else:

        messages.append(

            HumanMessage(
                content="Stop searching and return ONLY JSON."
            )

        )

        final_text = model.invoke(messages).content

    cleaned = final_text.strip()

    if cleaned.startswith("```"):

        cleaned = cleaned.replace("```json", "")

        cleaned = cleaned.replace("```", "")

    cleaned = cleaned.strip()

    parsed = json.loads(cleaned)

    return WebSearchReport(**parsed)