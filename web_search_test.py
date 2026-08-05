from agents.report_agent import run_report_agent


market_output = {
    "market_size": "Growing AI fitness market",
    "trends": ["AI personalization", "Wearables"]
}

competitor_output = {
    "competitors": ["Fitbod", "Freeletics"]
}

swot_output = {
    "strengths": ["AI customization"],
    "weaknesses": ["New product"],
    "opportunities": ["College fitness market"],
    "threats": ["Existing apps"]
}

mvp_output = {
    "features": [
        "AI workout planner",
        "Diet recommendation"
    ]
}

gtm_output = {
    "strategy": [
        "Target college students",
        "Campus marketing"
    ]
}


result = run_report_agent(
    market_output,
    competitor_output,
    swot_output,
    mvp_output,
    gtm_output
)


print(result)