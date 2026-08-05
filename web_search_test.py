from agents.web_search_agent import run_web_search_agent


startup_idea = """
AI-powered fitness assistant that generates
personalized workout plans and diet recommendations.
"""


result = run_web_search_agent(startup_idea)

print(result)