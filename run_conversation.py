from agents.conversational_advisor import run_conversational_advisor


THREAD_ID = "interactive-demo"


print("===================================")
print("   Conversational Advisor")
print("===================================")
print("Type 'exit' to stop.\n")


while True:
    user_message = input("You: ")

    if user_message.lower() == "exit":
        print("Conversation ended.")
        break

    response = run_conversational_advisor(
        user_message,
        thread_id=THREAD_ID,
    )

    print("\nAdvisor:")
    print(response["messages"][-1].content)
    print()