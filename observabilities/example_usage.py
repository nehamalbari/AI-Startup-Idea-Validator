"""
DeepAgents-only observability example.

This file does NOT change the existing application.

The existing application supplies the runtime values it already has, then
the independent observability DeepAgent analyzes them.
"""

import json
from observalities import run_observability

if __name__ == "__main__":
    report = run_observability(
        request="Validate the startup idea: AI platform for startup validation",
        response="The idea targets founders who need structured validation...",
        model_name="gemini-3.6-flash",
        input_tokens=450,
        output_tokens=700,
        total_tokens=1150,
        latency_ms=1840,
        temperature=0.3,
        request_count=1,
        trace_events=[
            {
                "name": "startup_validator",
                "kind": "agent",
                "status": "success",
                "latency_ms": 1840,
            }
        ],
    )
    print(json.dumps(report, indent=2))
