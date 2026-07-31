
"""
Market Analysis Agent

Flow:
1. Receive startup details
2. Use web search tool to collect information
3. Send search results to Groq
4. Generate market analysis JSON
"""


import os
import json

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from tools.web_search_tool import search_web
from state.schema import MarketAnalysis


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
You are a Market Analysis Agent.

Analyze startup opportunities using the provided web research.

Return ONLY valid JSON.

Format:

{
 "location":"string",
 "tam":"string",
 "sam":"string",
 "som":"string",
 "growth_rate":"string",
 "customer_segments":[
   {
    "name":"string",
    "description":"string"
   }
 ],
 "market_maturity":"Emerging | Growing | Mature | Declining",
 "key_trends":[
   "string"
 ]
}


Rules:

- TAM > SAM > SOM
- Use the provided research.
- Focus on target location.
- Avoid unrealistic numbers.
"""


# ---------------- FUNCTION ---------------- #

def run_market_analysis(
        startup_idea: str,
        industry: str,
        location: str
):

    # Step 1: Web Search

    search_query = f"""
    Market size, growth trends, customers,
    competitors for {startup_idea}
    in {location} {industry} industry
    """

    web_results = search_web.invoke(
    {
        "query": search_query
    }
)


    # Step 2: Send research to LLM

    messages = [

        SystemMessage(
            content=SYSTEM_PROMPT
        ),

        HumanMessage(
            content=f"""
Startup Idea:
{startup_idea}

Industry:
{industry}

Location:
{location}


Web Research:

{web_results}


Generate market analysis JSON.
"""
        )
    ]


    response = model.invoke(messages)


    output = response.content.strip()


    # Remove markdown

    if output.startswith("```"):

        output = output.replace("```json", "")
        output = output.replace("```", "")

    output = output.strip()


    data = json.loads(output)


    return MarketAnalysis(**data)

