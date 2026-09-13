from observability import (
    configure_langsmith,
    get_tracing_status,
    run_observable_pipeline,
)


def main():

    configure_langsmith()

    print("=" * 60)
    print("LANGSMITH OBSERVABILITY TEST")
    print("=" * 60)

    status = get_tracing_status()

    print("Tracing enabled:", status["enabled"])
    print("Project:", status["project"])
    print("API key configured:", status["api_key_configured"])

    print("=" * 60)

    startup_idea = (
        "AI platform that helps students validate startup ideas"
    )

    print("Running startup validation pipeline...")

    result = run_observable_pipeline(startup_idea)

    print("Pipeline completed successfully.")

    print("Result keys:")
    print(result.keys())


if __name__ == "__main__":
    main()