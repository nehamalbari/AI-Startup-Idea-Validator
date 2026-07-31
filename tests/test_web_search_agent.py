from agents.web_search_agent import run_web_search

idea = input("Enter Startup Idea: ")

report = run_web_search(idea)

print(report.model_dump_json(indent=4))