import json

from deepagents import create_deep_agent


with open("prompts/report_agent.md", "r") as file:
    system_prompt = file.read()


report_agent = create_deep_agent(
    system_prompt=system_prompt
)


def run_report_agent(
        market_output,
        competitor_output,
        swot_output,
        mvp_output,
        gtm_output
):

    report_input = {
        "market_analysis": market_output,
        "competitor_analysis": competitor_output,
        "swot_analysis": swot_output,
        "mvp_recommendation": mvp_output,
        "go_to_market_strategy": gtm_output
    }


    response = report_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": json.dumps(
                        report_input,
                        indent=4
                    )
                }
            ]
        }
    )


    content = response["messages"][-1].content


    if content.startswith("```json"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()


    return json.loads(content)