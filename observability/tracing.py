from .config import configure_langsmith


def tracing_status():
    """Return the current LangSmith tracing configuration."""
    return configure_langsmith()