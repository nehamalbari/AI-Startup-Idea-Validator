import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from tools.web_search_tool import search_web

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


# ---------------- PROMPT ---------------- #

SYSTEM_PROMPT = """
You are an AI SWOT & Risk Analysis Agent.

Analyze the startup idea using the provided web research.

Return the response in the following format.

Strengths
- Point 1
- Point 2
- Point 3

Weaknesses
- Point 1
- Point 2
- Point 3

Opportunities
- Point 1
- Point 2
- Point 3

Threats
- Point 1
- Point 2
- Point 3

Risk Analysis

Market Risks
- Point 1
- Point 2

Technical Risks
- Point 1
- Point 2

Financial Risks
- Point 1
- Point 2

Recommendations
- Point 1
- Point 2
- Point 3

Rules:
- Keep response under 350 words.
- Use short bullet points.
- No paragraphs.
- Be concise and professional.
"""


# ---------------- FUNCTION ---------------- #

def swot_risk_agent(startup_idea):

    search_query = f"""
    SWOT analysis, strengths, weaknesses,
    opportunities, threats,
    competitors, market risks,
    business risks for {startup_idea}
    """

    web_results = search_web.invoke(
        {
            "query": search_query
        }
    )

    messages = [

        SystemMessage(
            content=SYSTEM_PROMPT
        ),

        HumanMessage(
            content=f"""
Startup Idea:

{startup_idea}


Web Research:

{web_results}


Generate SWOT and Risk Analysis.
"""
        )

    ]

    response = model.invoke(messages)

    return response.content.strip()