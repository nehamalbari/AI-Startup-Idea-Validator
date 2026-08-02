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
from state.schema import SWOTRiskReport

load_dotenv()

# ---------------- API KEY ---------------- #

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY missing")

# ---------------- MODEL ---------------- #

model = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=GROQ_API_KEY,
    temperature=0.3
)

TOOLS = [search_web]

TOOLS_BY_NAME = {
    tool.name: tool
    for tool in TOOLS
}

model_with_tools = model.bind_tools(TOOLS)

MAX_STEPS = 5

# ---------------- PROMPT ---------------- #

SYSTEM_PROMPT = """
You are a Senior Business Strategy Consultant inside an AI Startup Validator.

Your task is to analyze the startup idea using autonomous web search.

You may search multiple times if needed.

Read all search results carefully.

Do NOT copy webpage titles or URLs.

Merge duplicate information into meaningful insights.

Return ONLY valid JSON.

{
    "strengths":[
        "...",
        "...",
        "..."
    ],
    "weaknesses":[
        "...",
        "...",
        "..."
    ],
    "opportunities":[
        "...",
        "...",
        "..."
    ],
    "threats":[
        "...",
        "...",
        "..."
    ],
    "market_risks":[
        "...",
        "..."
    ],
    "technical_risks":[
        "...",
        "..."
    ],
    "financial_risks":[
        "...",
        "..."
    ],
    "recommendations":[
        "...",
        "...",
        "..."
    ]
}

Rules:

- Return ONLY valid JSON.
- No markdown.
- No explanations outside JSON.
- No webpage titles.
- No URLs.
- Every point must be a complete business insight.
- Each point should contain around 15–25 words.
- Recommendations should be actionable.
- Maximum 3 items per SWOT category.
- Maximum 2 items per risk category.
"""

# ---------------- FUNCTION ---------------- #

def run_swot_analysis(startup_idea: str) -> SWOTRiskReport:

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),

        HumanMessage(
            content=f"""
Startup Idea

{startup_idea}

Perform SWOT analysis.
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

            tool = TOOLS_BY_NAME.get(tool_call["name"])

            if tool is None:
                result = "Unknown tool"

            else:
                result = tool.invoke(tool_call["args"])

            cleaned_result = " ".join(str(result).replace("\n", " ").split())

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

    return SWOTRiskReport(**parsed)