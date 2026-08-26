from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv

from .tracing import tracing_status

from deepagents import create_deep_agent

from .router import get_observability_model
from .tools import (
    build_trace,
    calculate_cost,
    collect_model_metrics,
    evaluate_performance,
    evaluate_quality_and_safety,
    record_errors,
    save_observability_report,
)

load_dotenv()
tracing_status()

SYSTEM_PROMPT = """
You are the DeepAgents metrics and quality runner for the AI Startup Idea Validator.

Observe one completed application run. Use ONLY the supplied observability
tools; do not use Python callbacks or callback handlers.

ARCHITECTURE

TIER 1 — MODEL METRICS
Tokens -> Latency -> Temperature -> Model Usage

TIER 2 — SYSTEM & QUALITY METRICS
Quality -> Cost -> Errors -> Tracing -> Performance -> Safety

API ROUTING
The observability model uses an isolated Gemini API-key router. If a Gemini
request is rate-limited or quota-exhausted, the router can fail over to the
next configured key. This does not increase provider quota; it prevents one
key from being a single point of failure.

LANGSMITH
Tracing is enabled through LangSmith environment configuration. Do not expose
API keys in reports.

WORKFLOW
1. Call collect_model_metrics using the supplied model/token/latency data.
2. Call calculate_cost using the supplied token data and pricing.
3. Call evaluate_quality_and_safety with the original request and response.
4. Make the quality/safety decision using the supplied material.
   quality_score must be 0-100.
   safety_status must be "safe" or "review".
   safety_flags must be an array.
5. Call record_errors.
6. Call build_trace.
7. Call evaluate_performance.
8. Produce one JSON report with exactly these top-level keys:
   trace_id
   agent_name
   tier_1_model_metrics
   tier_2_system_quality_metrics

The Tier 1 object must contain:
input_tokens, output_tokens, total_tokens, latency_ms, temperature,
model_name, request_count.

The Tier 2 object must contain:
quality_score, quality_reason, estimated_cost, errors, trace_count,
performance, safety_status, safety_flags, trace_spans.

Do not modify the user's existing application. You are an independent
metrics and quality runner.

Return ONLY valid JSON in your final answer.
"""


def create_metrics_runner(model=None):
    """Create the isolated DeepAgents metrics and quality runner."""
    return create_deep_agent(
        model=model or get_observability_model(),
        tools=[
            collect_model_metrics,
            calculate_cost,
            evaluate_quality_and_safety,
            record_errors,
            build_trace,
            evaluate_performance,
            save_observability_report,
        ],
        system_prompt=SYSTEM_PROMPT,
    )


_runner = None


def run_observability(
    request: Any,
    response: Any,
    *,
    model_name: str = "gemini-3.6-flash",
    input_tokens: int = 0,
    output_tokens: int = 0,
    total_tokens: int = 0,
    latency_ms: float = 0.0,
    temperature: Optional[float] = None,
    request_count: int = 1,
    error: Optional[str] = None,
    trace_events: Optional[list] = None,
    input_cost_per_1k: Optional[float] = None,
    output_cost_per_1k: Optional[float] = None,
    model=None,
    save: bool = True,
    log_path: str = "observalities/data/observability.jsonl",
) -> Dict[str, Any]:
    """Run the complete observability workflow through a DeepAgent."""
    global _runner
    if _runner is None or model is not None:
        _runner = create_metrics_runner(model)

    payload = {
        "request": request,
        "response": response,
        "model_name": model_name,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "latency_ms": latency_ms,
        "temperature": temperature,
        "request_count": request_count,
        "error": error,
        "trace_events": trace_events or [],
        "input_cost_per_1k": input_cost_per_1k,
        "output_cost_per_1k": output_cost_per_1k,
    }

    result = _runner.invoke({
        "messages": [{
            "role": "user",
            "content": json.dumps(payload, ensure_ascii=False, default=str),
        }]
    })

    content = result["messages"][-1].content
    if isinstance(content, list):
        content = "".join(
            item.get("text", "")
            for item in content
            if isinstance(item, dict)
        )

    text = str(content).strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        if text.endswith("```"):
            text = text[:-3].rstrip()

    report = json.loads(text)

    if save:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as file:
            file.write(json.dumps(report, ensure_ascii=False) + "\n")

    return report
