from agents.competitor_agent import competitor_agent


startup_idea = {
    "messages": [
        {
            "role": "user",
            "content": """
Startup Idea:
AI platform that helps students prepare for technical interviews.

Target Users:
College students and fresh graduates.

Industry:
EdTech
"""
        }
    ]
}


response = competitor_agent.invoke(startup_idea)

print(response["messages"][-1].content[0]["text"])