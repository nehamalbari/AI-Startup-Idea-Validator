import os
from dotenv import load_dotenv


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

ENV_FILE = os.path.join(PROJECT_ROOT, ".env")

load_dotenv(ENV_FILE)


def configure_langsmith():
    """Configure LangSmith tracing."""

    os.environ["LANGSMITH_TRACING"] = os.getenv(
        "LANGSMITH_TRACING",
        "true"
    )

    os.environ["LANGSMITH_PROJECT"] = os.getenv(
        "LANGSMITH_PROJECT",
        "AI-Startup-Idea-Validator"
    )

    return {
        "tracing_enabled": os.getenv(
            "LANGSMITH_TRACING",
            "false"
        ).lower() == "true",

        "project": os.getenv(
            "LANGSMITH_PROJECT",
            "AI-Startup-Idea-Validator"
        ),

        "api_key_configured": bool(
            os.getenv("LANGSMITH_API_KEY")
        ),
    }