import json
from agents.mvp_recommendation_agent import run_mvp_recommendation

if __name__ == "__main__":
    startup_idea = "AI Pitch Deck Generator for Early Stage Founders"
    target_audience = "Startup founders and solo entrepreneurs"
    industry = "SaaS / AI Tools"

    print(f"\n--- Testing Deep Agent with Idea...")
    result = run_mvp_recommendation(
        startup_idea=startup_idea,
        target_audience=target_audience,
        industry=industry
    )

    print("===== MVP RECOMMENDATION OUTPUT =====\n")
    print(result.model_dump_json(indent=4))