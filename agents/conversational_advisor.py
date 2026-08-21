import os

import psycopg
from dotenv import load_dotenv

from deepagents import create_deep_agent
from deepagents.backends import StateBackend
from deepagents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver

from app.config import llm

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env")


SYSTEM_PROMPT = """
You are the Conversational Advisor for an AI Startup Idea Validator.

Your role is to maintain a continuous conversation with the user
about their startup idea.

You should:

1. Remember important information from previous messages.
2. Use conversation history when answering follow-up questions.
3. Maintain continuity throughout the conversation.
4. Avoid asking the user to repeat information that is already available.
5. Give clear, practical and concise answers.
6. Use the latest information if the user changes their startup idea.
7. Help the user understand and validate their startup idea.
"""


backend = StateBackend()

summarization_middleware = SummarizationMiddleware(
    model=llm,
    backend=backend,
)

conversational_advisor = create_deep_agent(
    model=llm,
    system_prompt=SYSTEM_PROMPT,
    backend=backend,
    middleware=[
        summarization_middleware,
    ],
    checkpointer=InMemorySaver(),
)


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


def run_conversational_advisor(message, thread_id="default"):
    """
    Run the Conversational Advisor.

    PostgreSQL stores the conversation history so that
    history can be restored even after the application restarts.
    """

    history = get_history(thread_id)

    messages = history + [
        {
            "role": "user",
            "content": message,
        }
    ]

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

    save_message(
        thread_id,
        "user",
        message,
    )

    assistant_message = response["messages"][-1]

    content = assistant_message.content

    if isinstance(content, list):
        content = "".join(
            item.get("text", "")
            for item in content
            if isinstance(item, dict)
        )

    save_message(
        thread_id,
        "assistant",
        content,
    )

    return response