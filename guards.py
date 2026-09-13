"""
Local Safety Guardrails for AI Startup Validator.

All checks are local Python code.
No external Guardrails platform or API key is required.
"""

import re
from functools import wraps
from typing import Any, Callable

from pydantic import BaseModel, Field, ValidationError


# ============================================================
# 1. INPUT SAFETY GUARD
# ============================================================

def validate_input(startup_idea: str) -> tuple[bool, str]:
    """
    Checks whether the startup idea is safe and meaningful
    before it enters the agent pipeline.
    """

    if not startup_idea or not startup_idea.strip():
        return False, "Startup idea cannot be empty."

    idea = startup_idea.strip()

    # Prevent excessively large input.
    if len(idea) > 500:
        return False, "Startup idea is too long."

    # Reject meaningless input.
    if len(idea) < 5:
        return False, "Please provide a meaningful startup idea."

    # Basic prompt-injection detection.
    injection_patterns = [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"ignore\s+(all\s+)?above\s+instructions",
        r"system\s+prompt",
        r"reveal\s+(your|the)\s+(system\s+)?prompt",
        r"jailbreak",
        r"developer\s+message",
    ]

    for pattern in injection_patterns:
        if re.search(pattern, idea, re.IGNORECASE):
            return False, "Unsafe or malicious input detected."

    return True, "Input passed safety guard."


# ============================================================
# 2. OUTPUT STRUCTURAL GUARD
# ============================================================

class StartupValidationReport(BaseModel):
    """
    Expected structure of the final startup validation report.
    """

    startup_overview: dict[str, Any]
    market_analysis: dict[str, Any]
    competitor_analysis: dict[str, Any]
    swot_analysis: dict[str, Any]
    mvp_recommendation: dict[str, Any]
    go_to_market: dict[str, Any]
    final_recommendation: dict[str, Any]


def validate_output(output: Any) -> tuple[bool, str]:
    """
    Validates the final agent output against the Pydantic schema.
    """

    try:
        StartupValidationReport.model_validate(output)
        return True, "Output passed safety and structure validation."

    except ValidationError as error:
        return False, f"Output validation failed: {error}"


# ============================================================
# 3. SENSITIVE DATA GUARD
# ============================================================

def check_sensitive_data(text: str) -> tuple[bool, str]:
    """
    Detects common secrets that should not appear in output.
    """

    secret_patterns = [
        r"sk-[A-Za-z0-9_-]{20,}",       # OpenAI-style API key
        r"api[_-]?key\s*[:=]\s*\S+",
        r"password\s*[:=]\s*\S+",
        r"secret\s*[:=]\s*\S+",
    ]

    for pattern in secret_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False, "Sensitive information detected in output."

    return True, "No obvious sensitive information detected."


# ============================================================
# 4. LOOP PREVENTION GUARD
# ============================================================

def limit_agent_loops(max_loops: int = 5):
    """
    Prevents an orchestration function from exceeding
    the configured number of agent interactions.
    """

    def decorator(func: Callable):

        @wraps(func)
        def wrapper(*args, **kwargs):

            for interaction_count in range(1, max_loops + 1):

                result = func(
                    *args,
                    interaction_count=interaction_count,
                    **kwargs
                )

                if result is not None:
                    return result

            return (
                "Process stopped safely: maximum agent "
                "interaction limit reached."
            )

        return wrapper

    return decorator


# ============================================================
# 5. SELF-CORRECTION GUARD
# ============================================================

def self_correct(
    data: Any,
    retry_function: Callable,
    max_retries: int = 2
) -> StartupValidationReport | None:
    """
    Attempts to correct invalid agent output.

    Maximum retry attempts: 2.
    """

    current_data = data

    for attempt in range(max_retries + 1):

        try:
            return StartupValidationReport.model_validate(
                current_data
            )

        except ValidationError as error:

            if attempt >= max_retries:
                return None

            current_data = retry_function(
                current_data,
                str(error)
            )

    return None