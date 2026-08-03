import json
from agents.mvp_recommendation_agent import run_mvp_recommendation


def test_mvp_agent():
    startup_idea = "AI Resume Builder for Students"
    target_audience = "College students and recent graduates"
    industry = "EdTech / HR Tech"

    print(f"\n--- Testing Deep Agent with Idea: '{startup_idea}' ---")
   
    result = run_mvp_recommendation(
        startup_idea=startup_idea,
        target_audience=target_audience,
        industry=industry
    )

    print("\n===== MVP RECOMMENDATION OUTPUT =====\n")
    print(result.model_dump_json(indent=4))


if __name__ == "__main__":
    test_mvp_agent()