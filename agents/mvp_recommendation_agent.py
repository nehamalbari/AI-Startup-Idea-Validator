import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from deepagents import create_deep_agent

from tools.web_search_tool import search_web
from state.mvp_recommendation_schema import MVPRecommendation

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

model = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=GROQ_API_KEY,
    temperature=0.1,
)

prompt_path = Path(__file__).parent.parent / "prompts" / "mvp_agent.md"
with open(prompt_path, "r", encoding="utf-8") as f:
    MVP_AGENT_SYSTEM_PROMPT = f.read()

mvp_deep_agent = create_deep_agent(
    model=model,
    tools=[search_web],
    system_prompt=MVP_AGENT_SYSTEM_PROMPT,
    response_format=MVPRecommendation,
)

def run_mvp_recommendation(
    startup_idea: str,
    target_audience: str = None,
    industry: str = None,
    constraints: str = None,
) -> MVPRecommendation:
    task_input = f"""
Startup Idea: {startup_idea}
Target Audience: {target_audience or 'N/A'}
Industry: {industry or 'N/A'}
Constraints: {constraints or 'N/A'}

Follow the workflow exactly:
1. Create or update plan.md with a short execution plan.
2. Use search_web 2 to 3 times to research competitors, existing solutions, and MVP patterns.
3. Save detailed findings to research_notes.md.
4. Draft a concrete MVP recommendation in mvp_draft.md.
5. Return the final recommendation in the required structured format.

Rules:
- Be specific and technical.
- Every feature must name concrete tools, workflows, or interfaces.
- Avoid generic filler.
- Keep scope to 4-6 weeks for a small engineering team.
""".strip()

    result = mvp_deep_agent.invoke(
        {"messages": [{"role": "user", "content": task_input}]}
    )

    structured = result.get("structured_response")
    if structured is None:
        raise RuntimeError("Deep agent did not return a structured_response.")

    return structured