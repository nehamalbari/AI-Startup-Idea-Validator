from agents.conversational_advisor import run_conversational_advisor


def get_text(response):
    """Extract text from the latest assistant message."""
    content = response["messages"][-1].content

    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict) and "text" in item:
                return item["text"]
        return str(content)

    return str(content)


def test_basic_conversation():
    response = run_conversational_advisor(
        "My startup idea is an AI resume builder for students.",
        "test-basic"
    )

    text = get_text(response)

    assert text
    assert len(text) > 0

    print("\nBasic conversation test: PASSED")


def test_conversation_memory():
    thread_id = "test-memory-automated"

    run_conversational_advisor(
        "My startup idea is an AI resume builder for students.",
        thread_id
    )

    response = run_conversational_advisor(
        "Who are my target users?",
        thread_id
    )

    text = get_text(response).lower()

    assert "student" in text

    print("\nConversation memory test: PASSED")


def test_multi_turn_memory():
    thread_id = "test-multi-turn"

    run_conversational_advisor(
        "My startup idea is an AI resume builder for students.",
        thread_id
    )

    run_conversational_advisor(
        "I want to focus on final-year engineering students.",
        thread_id
    )

    response = run_conversational_advisor(
        "What problem am I solving?",
        thread_id
    )

    text = get_text(response).lower()

    assert "engineering" in text or "student" in text
    assert "resume" in text

    print("\nMulti-turn memory test: PASSED")


def test_startup_idea_change():
    thread_id = "test-idea-change"

    run_conversational_advisor(
        "My startup idea is an AI resume builder for students.",
        thread_id
    )

    run_conversational_advisor(
        "I changed my startup idea. Now I want to build "
        "an AI-powered platform that helps small businesses "
        "predict customer demand.",
        thread_id
    )

    response = run_conversational_advisor(
        "What is my current startup idea?",
        thread_id
    )

    text = get_text(response).lower()

    assert "small business" in text
    assert "customer demand" in text

    print("\nStartup idea change test: PASSED")


if __name__ == "__main__":
    test_basic_conversation()
    test_conversation_memory()
    test_multi_turn_memory()
    test_startup_idea_change()

    print("\n===================================")
    print("ALL CONVERSATIONAL ADVISOR TESTS PASSED")
    print("===================================")