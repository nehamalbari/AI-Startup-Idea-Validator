import json

from deepagents import create_deep_agent

from app.config import llm
from tools.pdf_generation_tool import pdf_generation_tool


with open("prompts/pdf_generation_agent.md", "r") as file:
    system_prompt = file.read()


pdf_generation_agent = create_deep_agent(
    model=llm,
    system_prompt=system_prompt,
    tools=[pdf_generation_tool]
)


def run_pdf_generation_agent(report_data):

    response = pdf_generation_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": json.dumps(
                        report_data,
                        indent=4
                    )
                }
            ]
        }
    )

    content = response["messages"][-1].content

    if isinstance(content, list):
        content = content[0]["text"]

    return content.strip()