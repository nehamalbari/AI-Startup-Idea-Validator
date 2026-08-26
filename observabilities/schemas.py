from __future__ import annotations
from typing import Any, Dict, List, Optional, TypedDict

class ObservabilityInput(TypedDict, total=False):
    request: Any
    response: Any
    model_name: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    latency_ms: float
    temperature: Optional[float]
    request_count: int
    error: Optional[str]
    trace_events: List[Dict[str, Any]]
    input_cost_per_1k: Optional[float]
    output_cost_per_1k: Optional[float]

class ObservabilityReport(TypedDict):
    tier_1_model_metrics: Dict[str, Any]
    tier_2_system_quality_metrics: Dict[str, Any]
    trace_id: str
