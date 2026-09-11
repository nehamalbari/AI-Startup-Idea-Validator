import time

from langsmith import traceable

from .config import configure_langsmith

# Configure LangSmith BEFORE importing the application agents.
configure_langsmith()

from agents.web_search_agent import run_web_search_agent
from agents.market_analysis_agent import run_market_agent
from agents.competitor_agent import run_competitor_agent
from agents.swot_risk_agent import run_swot_agent
from agents.mvp_recommendation_agent import run_mvp_agent
from agents.gtm_strategy_agent import run_gtm_agent
from agents.report_agent import run_report_agent
from agents.pdf_generation_agent import run_pdf_generation_agent


# ---------------------------------------------------------
# Retry helper for transient connection errors only.
# Quota errors (429 / RESOURCE_EXHAUSTED) are NOT retried here --
# app/config.py's key rotation already handles those, and retrying
# a call that's already out of quota just wastes time.
# ---------------------------------------------------------

CONNECTION_ERROR_MARKERS = (
    "10054",
    "ConnectionError",
    "ReadError",
    "RemoteDisconnected",
    "Connection aborted",
)


def _is_connection_error(error):
    error_text = str(error)
    return any(marker in error_text for marker in CONNECTION_ERROR_MARKERS)


def _with_retry(func, *args, max_retries=2, delay_seconds=3, **kwargs):
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            last_error = error

            if not _is_connection_error(error):
                raise

            if attempt < max_retries:
                print(
                    f"[Observability Retry] Connection error on attempt "
                    f"{attempt}/{max_retries}: {error}. "
                    f"Retrying in {delay_seconds}s..."
                )
                time.sleep(delay_seconds)
            else:
                print(
                    f"[Observability Retry] Connection error persisted "
                    f"after {max_retries} attempts."
                )

    raise last_error


# ---------------------------------------------------------
# Individual traced agent functions
# ---------------------------------------------------------

@traceable(name="Web Search Agent", run_type="chain")
def trace_web_search(startup_idea):
    return _with_retry(run_web_search_agent, startup_idea)


@traceable(name="Market Analysis Agent", run_type="chain")
def trace_market_analysis(web_output):
    return _with_retry(run_market_agent, web_output)


@traceable(name="Competitor Analysis Agent", run_type="chain")
def trace_competitor_analysis(market_output):
    return _with_retry(run_competitor_agent, market_output)


@traceable(name="SWOT Risk Agent", run_type="chain")
def trace_swot_risk(competitor_output):
    return _with_retry(run_swot_agent, competitor_output)


@traceable(name="MVP Recommendation Agent", run_type="chain")
def trace_mvp_recommendation(swot_output):
    return _with_retry(run_mvp_agent, swot_output)


@traceable(name="GTM Strategy Agent", run_type="chain")
def trace_gtm_strategy(mvp_output):
    return _with_retry(run_gtm_agent, mvp_output)


@traceable(name="Report Agent", run_type="chain")
def trace_report(
    market_output,
    competitor_output,
    swot_output,
    mvp_output,
    gtm_output
):
    return _with_retry(
        run_report_agent,
        market_output,
        competitor_output,
        swot_output,
        mvp_output,
        gtm_output
    )


@traceable(name="PDF Generation Agent", run_type="chain")
def trace_pdf_generation(report_output):
    return _with_retry(run_pdf_generation_agent, report_output)


# ---------------------------------------------------------
# Main observable pipeline
# ---------------------------------------------------------

@traceable(name="AI Startup Idea Validator", run_type="chain")
def run_observable_pipeline(startup_idea):
    """
    Run the existing startup validation pipeline
    with LangSmith tracing around every major agent.
    """

    web_output = trace_web_search(startup_idea)

    market_output = trace_market_analysis(web_output)

    competitor_output = trace_competitor_analysis(market_output)

    swot_output = trace_swot_risk(competitor_output)

    mvp_output = trace_mvp_recommendation(swot_output)

    gtm_output = trace_gtm_strategy(mvp_output)

    report_output = trace_report(
        market_output,
        competitor_output,
        swot_output,
        mvp_output,
        gtm_output
    )

    pdf_output = trace_pdf_generation(report_output)

    return {
        "report": report_output,
        "pdf": pdf_output
    }