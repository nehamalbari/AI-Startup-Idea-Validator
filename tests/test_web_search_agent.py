from agents.web_search_agent import run_web_search


def main():

    startup_idea = input("Enter Startup Idea: ")

    print("\nSearching...\n")

    report = run_web_search(startup_idea)

    print(report)


if __name__ == "__main__":
    main()