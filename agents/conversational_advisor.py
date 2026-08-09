import os

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