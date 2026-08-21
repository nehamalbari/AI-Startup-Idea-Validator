from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends import StateBackend
from deepagents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver

from app.config import llm
from tools.postgres_memory import get_messages, save_message


# --------------------------------------------------
# Load system prompt from prompt file
# --------------------------------------------------

PROMPT_FILE = (
    Path(__file__).resolve().parent.parent
    / "prompts"
    / "conversational_adviser.md"
)

if not PROMPT_FILE.exists():
    raise FileNotFoundError(
        f"Prompt file not found: {PROMPT_FILE}"
    )

SYSTEM_PROMPT = PROMPT_FILE.read_text(
    encoding="utf-8"
)


# --------------------------------------------------
# Backend
# --------------------------------------------------

backend = StateBackend()


# --------------------------------------------------
# Summarization middleware
# --------------------------------------------------

summarization_middleware = SummarizationMiddleware(
    model=llm,
    backend=backend,
)


# --------------------------------------------------
# Create Conversational Advisor
# --------------------------------------------------

conversational_advisor = create_deep_agent(
    model=llm,
    system_prompt=SYSTEM_PROMPT,
    backend=backend,
    middleware=[
        summarization_middleware,
    ],
    checkpointer=InMemorySaver(),
)


# --------------------------------------------------
# Run Conversational Advisor
# --------------------------------------------------

def run_conversational_advisor(message, thread_id="default"):
    """
    Run the Conversational Advisor.

    PostgreSQL stores the conversation history so that
    history can be restored even after the application
    restarts.
    """

    # --------------------------------------------------
    # Get previous conversation history
    # --------------------------------------------------

    history = get_messages(thread_id)

    # --------------------------------------------------
    # Add current user message for the agent
    # --------------------------------------------------

    messages = history + [
        {
            "role": "user",
            "content": message,
        }
    ]

    # --------------------------------------------------
    # Save user message to PostgreSQL
    # --------------------------------------------------

    save_message(
        thread_id,
        "user",
        message,
    )

    # --------------------------------------------------
    # Run the agent
    # --------------------------------------------------

    response = conversational_advisor.invoke(
        {
            "messages": messages,
        },
        config={
            "configurable": {
                "thread_id": thread_id,
            }
        },
    )

    # --------------------------------------------------
    # Get latest assistant response
    # --------------------------------------------------

    assistant_message = response["messages"][-1]

    content = assistant_message.content

    # --------------------------------------------------
    # Handle structured Gemini response
    # --------------------------------------------------

    if isinstance(content, list):
        content = "".join(
            item.get("text", "")
            for item in content
            if isinstance(item, dict)
        )

    # --------------------------------------------------
    # Save assistant response to PostgreSQL
    # --------------------------------------------------

    save_message(
        thread_id,
        "assistant",
        content,
    )

    return response