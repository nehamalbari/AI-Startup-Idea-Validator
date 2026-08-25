"""LangSmith tracing setup for the isolated observability layer."""
from __future__ import annotations

import os
from dotenv import load_dotenv

load_dotenv()

# LangChain/DeepAgents automatically picks these environment variables up.
# No LangSmith key is stored in source code.
os.environ.setdefault("LANGSMITH_TRACING", "true")
os.environ.setdefault(
    "LANGSMITH_PROJECT",
    "AI-Startup-Idea-Validator-Observability",
)


def tracing_status():
    """Return non-secret LangSmith configuration status."""
    return {
        "enabled": os.getenv("LANGSMITH_TRACING", "false").lower() == "true",
        "project": os.getenv(
            "LANGSMITH_PROJECT",
            "AI-Startup-Idea-Validator-Observability",
        ),
        "api_key_configured": bool(os.getenv("LANGSMITH_API_KEY")),
    }
