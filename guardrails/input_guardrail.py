def validate_startup_idea(startup_idea: str):
    """
    Validate user input before starting the agent pipeline.
    """

    if not startup_idea or not startup_idea.strip():
        return False, "Startup idea cannot be empty."

    idea = startup_idea.strip()

    if len(idea) < 5:
        return False, "Please provide a meaningful startup idea."

    if len(idea) > 500:
        return False, "Startup idea must be less than 500 characters."

    # Reject obvious non-startup/test inputs
    invalid_inputs = {
        "hi",
        "hello",
        "hey",
        "test",
        "asdf",
        "asdfgh",
        "12345"
    }

    if idea.lower() in invalid_inputs:
        return False, "Please provide a valid startup idea."

    return True, "Input passed guardrail."