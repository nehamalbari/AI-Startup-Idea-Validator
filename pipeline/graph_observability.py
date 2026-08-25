from __future__ import annotations

import json
import time
from typing import Any, Dict, List, Tuple

from agents.web_search_agent import web_search_agent
from agents.market_analysis_agent import market_agent
from agents.competitor_agent import competitor_agent
from agents.swot_risk_agent import swot_agent
from agents.mvp_recommendation_agent import mvp_agent
from agents.gtm_strategy_agent import gtm_agent
from agents.report_agent import report_agent
from agents.pdf_generation_agent import pdf_generation_agent

from observalities import run_observability


def _extract_text(content: Any) -> str:
    """Same extraction logic used across agents/*.py, kept identical here."""
    if isinstance(content, list):
        extracted = ""
        for item in content:
            if isinstance(item, dict) and "text" in item:
                extracted += item["text"]
        content = extracted
    content = str(content).strip()
    if content.startswith("```json"):
        content = content.replace("```json", "", 1)
    if content.endswith("```"):
        content = content[:-3]
    return content.strip()


def _extract_usage(response: Dict[str, Any]) -> Tuple[int, int, int]:
    """Pull real token usage off the LangChain AIMessage if the provider set it."""
    try:
        last_message = response["messages"][-1]
        usage = getattr(last_message, "usage_metadata", None)
        if usage:
            input_tokens = usage.get("input_tokens", 0) or 0
            output_tokens = usage.get("output_tokens", 0) or 0
            total_tokens = usage.get("total_tokens", input_tokens + output_tokens)
            return input_tokens, output_tokens, total_tokens
    except Exception:
        pass
    return 0, 0, 0


def _run_step(
    agent_name: str,
    agent,
    user_content: str,
    parse_json: bool = True,
) -> Tuple[Any, Dict[str, Any]]:
    """Invoke one agent, time it, pull real usage, and run observability on it."""
    started = time.time()
    response = agent.invoke(
        {"messages": [{"role": "user", "content": user_content}]}
    )
    latency_ms = round((time.time() - started) * 1000, 2)

    raw_content = response["messages"][-1].content
    text = _extract_text(raw_content)
    result = json.loads(text) if parse_json else text

    input_tokens, output_tokens, total_tokens = _extract_usage(response)

    report = run_observability(
        request=user_content,
        response=text,
        model_name="gemini-3.6-flash",
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        latency_ms=latency_ms,
        temperature=0.3,
        request_count=1,
        trace_events=[
            {
                "name": agent_name,
                "kind": "agent",
                "status": "success",
                "latency_ms": latency_ms,
            }
        ],
    )
    report["agent_name"] = agent_name

    return result, report


def run_pipeline_with_observability(startup_idea: str) -> Dict[str, Any]:
    """Run all 8 agents and collect a Tier 1 / Tier 2 report for each one."""
    reports: List[Dict[str, Any]] = []

    # Step 1: Web Search
    web_output, r1 = _run_step(
        "web_search_agent",
        web_search_agent,
        f"""
Startup Idea:

{startup_idea}

Search the web and return the result in JSON format.
""",
    )
    reports.append(r1)

    # Step 2: Market Analysis
    market_output, r2 = _run_step(
        "market_analysis_agent",
        market_agent,
        json.dumps(web_output, indent=4),
    )
    reports.append(r2)

    # Step 3: Competitor Analysis
    competitor_output, r3 = _run_step(
        "competitor_agent",
        competitor_agent,
        json.dumps(market_output, indent=4),
    )
    reports.append(r3)

    # Step 4: SWOT Analysis
    swot_output, r4 = _run_step(
        "swot_risk_agent",
        swot_agent,
        json.dumps(competitor_output, indent=4),
    )
    reports.append(r4)

    # Step 5: MVP Recommendation
    mvp_output, r5 = _run_step(
        "mvp_recommendation_agent",
        mvp_agent,
        json.dumps(swot_output, indent=4),
    )
    reports.append(r5)

    # Step 6: Go-To-Market Strategy
    gtm_output, r6 = _run_step(
        "gtm_strategy_agent",
        gtm_agent,
        json.dumps(mvp_output, indent=4),
    )
    reports.append(r6)

    # Step 7: Final Report
    report_input = {
        "market_analysis": market_output,
        "competitor_analysis": competitor_output,
        "swot_analysis": swot_output,
        "mvp_recommendation": mvp_output,
        "go_to_market_strategy": gtm_output,
    }
    report_output, r7 = _run_step(
        "report_agent",
        report_agent,
        json.dumps(report_input, indent=4),
    )
    reports.append(r7)

    # Step 8: PDF Generation (returns plain text, not JSON)
    pdf_output, r8 = _run_step(
        "pdf_generation_agent",
        pdf_generation_agent,
        json.dumps(report_output, indent=4),
        parse_json=False,
    )
    reports.append(r8)

    return {
        "report": report_output,
        "pdf": pdf_output,
        "observability": {
            "tier_1_model_metrics": [r["tier_1_model_metrics"] for r in reports],
            "tier_2_system_quality_metrics": [r["tier_2_system_quality_metrics"] for r in reports],
            "per_agent_reports": reports,
        },
    }


if __name__ == "__main__":
    idea = "AI platform for startup validation"
    result = run_pipeline_with_observability(idea)
    print(json.dumps(result["observability"], indent=2))