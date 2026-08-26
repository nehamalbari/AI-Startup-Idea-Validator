from __future__ import annotations

import json
import time
import uuid
from typing import Any, Dict, List, Optional

from langchain_core.tools import tool

from .config import (
    DEFAULT_TEMPERATURE,
    INPUT_COST_PER_1K,
    OUTPUT_COST_PER_1K,
)

def _trace_id() -> str:
    return uuid.uuid4().hex

@tool
def collect_model_metrics(
    input_tokens: int = 0,
    output_tokens: int = 0,
    total_tokens: int = 0,
    latency_ms: float = 0.0,
    temperature: Optional[float] = None,
    model_name: str = "unknown",
    request_count: int = 1,
) -> Dict[str, Any]:
    """Collect Tier 1 model metrics: tokens, latency, temperature and model usage."""
    if total_tokens == 0:
        total_tokens = input_tokens + output_tokens
    if temperature is None:
        temperature = DEFAULT_TEMPERATURE

    return {
        "input_tokens": max(0, input_tokens),
        "output_tokens": max(0, output_tokens),
        "total_tokens": max(0, total_tokens),
        "latency_ms": round(max(0.0, latency_ms), 2),
        "temperature": temperature,
        "model_name": model_name,
        "request_count": max(0, request_count),
    }

@tool
def calculate_cost(
    input_tokens: int = 0,
    output_tokens: int = 0,
    input_cost_per_1k: Optional[float] = None,
    output_cost_per_1k: Optional[float] = None,
) -> Dict[str, Any]:
    """Calculate estimated LLM cost for Tier 2 from supplied token usage and pricing."""
    in_price = INPUT_COST_PER_1K if input_cost_per_1k is None else input_cost_per_1k
    out_price = OUTPUT_COST_PER_1K if output_cost_per_1k is None else output_cost_per_1k

    if in_price is None or out_price is None:
        return {
            "estimated_cost": None,
            "currency": "USD",
            "status": "pricing_not_configured",
        }

    cost = (input_tokens / 1000.0) * in_price
    cost += (output_tokens / 1000.0) * out_price
    return {
        "estimated_cost": round(cost, 8),
        "currency": "USD",
        "status": "calculated",
    }

@tool
def evaluate_quality_and_safety(
    request: str,
    response: str,
) -> Dict[str, Any]:
    """Evaluate response quality and safety for Tier 2. Returns a 0-100 quality score."""
    prompt = (
        "Evaluate this AI startup validator response. "
        "Score relevance, completeness, usefulness, consistency and grounding. "
        "Also identify obvious safety concerns. "
        "Return JSON only with keys: quality_score (0-100), "
        "quality_reason, safety_status (safe/review), safety_flags (array).\\n\\n"
        f"REQUEST:\\n{request}\\n\\nRESPONSE:\\n{response}"
    )
    # This tool is intentionally deterministic and local: the DeepAgent's model
    # performs the evaluation through its own tool execution context.
    # The semantic evaluation is instructed in the DeepAgents system prompt,
    # so this tool records the raw material for that decision.
    return {
        "evaluation_request": prompt,
        "quality_score": None,
        "quality_reason": "Pending DeepAgent evaluation.",
        "safety_status": "pending",
        "safety_flags": [],
    }

@tool
def record_errors(error: Optional[str] = None, error_type: str = "runtime") -> Dict[str, Any]:
    """Record Tier 2 errors. Pass an empty error when the run succeeded."""
    if not error:
        return {"error_count": 0, "errors": []}
    return {
        "error_count": 1,
        "errors": [{"type": error_type, "message": error}],
    }

@tool
def build_trace(
    events: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Build Tier 2 tracing information from application-supplied events."""
    trace_id = _trace_id()
    normalized = []
    for index, event in enumerate(events or []):
        normalized.append({
            "span_id": str(event.get("span_id", index + 1)),
            "name": str(event.get("name", "unknown")),
            "kind": str(event.get("kind", "agent")),
            "status": str(event.get("status", "success")),
            "latency_ms": event.get("latency_ms"),
            "metadata": event.get("metadata", {}),
        })

    return {
        "trace_id": trace_id,
        "trace_count": len(normalized),
        "spans": normalized,
    }

@tool
def evaluate_performance(
    end_to_end_latency_ms: float,
    expected_latency_ms: float = 5000.0,
) -> Dict[str, Any]:
    """Evaluate Tier 2 performance against an expected latency threshold."""
    latency = max(0.0, end_to_end_latency_ms)
    threshold = max(1.0, expected_latency_ms)
    if latency <= threshold:
        status = "good"
    elif latency <= threshold * 2:
        status = "degraded"
    else:
        status = "poor"

    return {
        "end_to_end_latency_ms": round(latency, 2),
        "expected_latency_ms": round(threshold, 2),
        "status": status,
    }

@tool
def save_observability_report(report_json: str, path: str = "observalities/data/observability.jsonl") -> Dict[str, Any]:
    """Persist the final DeepAgent-generated observability report as JSONL."""
    try:
        report = json.loads(report_json)
        with open(path, "a", encoding="utf-8") as file:
            file.write(json.dumps(report, ensure_ascii=False, default=str) + "\\n")
        return {"saved": True, "path": path}
    except Exception as exc:
        return {"saved": False, "error": str(exc)}
