import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def _database_is_configured() -> bool:
    """Return whether persistent chat storage has been configured."""
    return bool(DATABASE_URL)


def save_message(thread_id, role, content):
    """Persist a message when PostgreSQL is configured."""

    if not _database_is_configured():
        return

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


def get_messages(thread_id):
    """Return persisted messages, or an empty history when no database is set."""

    if not _database_is_configured():
        return []

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT role, content
                FROM conversation_messages
                WHERE thread_id = %s
                ORDER BY id ASC
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