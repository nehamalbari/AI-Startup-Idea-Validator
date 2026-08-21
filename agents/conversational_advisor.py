import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

from deepagents import create_deep_agent
from deepagents.backends import StateBackend
from deepagents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver

from app.config import llm


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env")


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
# PostgreSQL: Get conversation history
# --------------------------------------------------

def get_history(thread_id):
    """Get previous conversation messages from PostgreSQL."""

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT role, content
                FROM conversation_messages
                WHERE thread_id = %s
                ORDER BY created_at ASC, id ASC
                """,
                (thread_id,),
            )

            rows = cur.fetchall()

    return [
        {
            "role": role,
            "content": content,
        }
        for role, content in rows
    ]


# --------------------------------------------------
# PostgreSQL: Save conversation message
# --------------------------------------------------

def save_message(thread_id, role, content):
    """Save one conversation message to PostgreSQL."""

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO conversation_messages
                    (thread_id, role, content)
                VALUES
                    (%s, %s, %s)
                """,
                (thread_id, role, content),
            )


# --------------------------------------------------
# Run Conversational Advisor
# --------------------------------------------------

def run_conversational_advisor(message, thread_id="default"):
    """
    Run the Conversational Advisor.

    PostgreSQL stores the conversation history so that
    history can be restored even after the application restarts.
    """

    # Get previous conversation history
    history = get_history(thread_id)

    # Add current user message
    messages = history + [
        {
            "role": "user",
            "content": message,
        }
    ]

    # Run the agent
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

    # Save user message
    save_message(
        thread_id,
        "user",
        message,
    )

    # Get latest assistant response
    assistant_message = response["messages"][-1]

    content = assistant_message.content

    # Handle structured Gemini response
    if isinstance(content, list):
        content = "".join(
            item.get("text", "")
            for item in content
            if isinstance(item, dict)
        )

    # Save assistant response
    save_message(
        thread_id,
        "assistant",
        content,
    )

    return response