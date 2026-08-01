from agents.swot_risk_agent import swot_risk_agent

idea = input("Enter Startup Idea: ")

report = swot_risk_agent(idea)

print("\n" + "=" * 80)
print("SWOT & RISK ANALYSIS REPORT")
print("=" * 80)
print(report)