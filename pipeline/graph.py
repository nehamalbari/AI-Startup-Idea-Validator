from agents.web_search_agent import run_web_search_agent
from agents.market_analysis_agent import run_market_agent
from agents.competitor_agent import run_competitor_agent
from agents.swot_risk_agent import run_swot_agent
from agents.mvp_recommendation_agent import run_mvp_agent
from agents.gtm_strategy_agent import run_gtm_agent
from agents.report_agent import run_report_agent


def run_pipeline(startup_idea):

    # Step 1: Web Search
    web_output = run_web_search_agent(
        startup_idea
    )


    # Step 2: Market Analysis
    market_output = run_market_agent(
        startup_idea,
        web_output
    )


    # Step 3: Competitor Analysis
    competitor_output = run_competitor_agent(
        startup_idea,
        web_output
    )


    # Step 4: SWOT Analysis
    swot_output = run_swot_agent(
        market_output,
        competitor_output
    )


    # Step 5: MVP Recommendation
    mvp_output = run_mvp_agent(
        startup_idea,
        swot_output,
        market_output
    )


    # Step 6: Go-To-Market Strategy
    gtm_output = run_gtm_agent(
        startup_idea,
        market_output,
        competitor_output,
        mvp_output
    )


    # Step 7: Final Report
    report_output = run_report_agent(
        market_output,
        competitor_output,
        swot_output,
        mvp_output,
        gtm_output
    )


    return report_output