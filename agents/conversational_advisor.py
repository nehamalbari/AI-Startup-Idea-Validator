import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from deepagents import create_deep_agent
from deepagents.backends import StateBackend
from deepagents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver


load_dotenv()


# Separate LLM configuration ONLY for Conversational Advisor

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)


# Load system prompt from prompts/conversational_adviser.md

PROMPT_PATH = (
    Path(__file__).resolve().parent.parent
    / "prompts"
    / "conversational_adviser.md"
)

SYSTEM_PROMPT = PROMPT_PATH.read_text(encoding="utf-8")


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


def run_conversational_advisor(message, thread_id="default"):
    """
    Run the Conversational Advisor.

    The thread_id identifies the conversation so that
    previous messages can be retrieved on subsequent calls.
    """

    response = conversational_advisor.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": message,
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": thread_id,
            }
        },
    )

    return response