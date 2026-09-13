from observability.tracing import tracing_status
from observability.runner import run_observable_pipeline


def main():

    print("=" * 60)
    print("LANGSMITH OBSERVABILITY TEST")
    print("=" * 60)

    status = tracing_status()

    print(
        f"Tracing enabled: {status['tracing_enabled']}"
    )

    print(
        f"Project: {status['project']}"
    )

    print(
        f"API key configured: {status['api_key_configured']}"
    )

    print("=" * 60)

    startup_idea = (
        "An AI-powered platform that helps small businesses "
        "validate startup ideas, analyze competitors, "
        "understand market opportunities, and recommend "
        "an MVP."
    )

    print("Running startup validation pipeline...")
    print()

    try:

        result = run_observable_pipeline(
            startup_idea
        )

        print()
        print("=" * 60)
        print("PIPELINE COMPLETED")
        print("=" * 60)

        if result:
            print("Report generated:", "report" in result)
            print("PDF generated:", "pdf" in result)

        print()
        print(
            "Check LangSmith to view the complete trace."
        )

    except Exception as error:

        print()
        print("=" * 60)
        print("PIPELINE FAILED")
        print("=" * 60)

        print(
            f"{type(error).__name__}: {error}"
        )

        print()
        print(
            "The LangSmith trace should contain the "
            "failed agent/span."
        )


if __name__ == "__main__":
    main()