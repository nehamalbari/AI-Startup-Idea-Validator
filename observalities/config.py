"""Observability-only configuration.

The existing application configuration is intentionally untouched.
"""
import os
from dotenv import load_dotenv

load_dotenv()

OBS_INPUT_COST_PER_1K = os.getenv("OBS_INPUT_COST_PER_1K")
OBS_OUTPUT_COST_PER_1K = os.getenv("OBS_OUTPUT_COST_PER_1K")
OBS_MODEL_NAME = os.getenv("OBS_MODEL_NAME", "gemini-3.6-flash")
OBS_TEMPERATURE = os.getenv("OBS_TEMPERATURE", "0")

LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "true")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "AI-Startup-Idea-Validator-Observability")


def as_float(value):
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


INPUT_COST_PER_1K = as_float(OBS_INPUT_COST_PER_1K)
OUTPUT_COST_PER_1K = as_float(OBS_OUTPUT_COST_PER_1K)
DEFAULT_TEMPERATURE = as_float(OBS_TEMPERATURE)
