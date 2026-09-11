from agents.market_analysis_agent import run_market_analysis

print("=" * 60)
print("AI STARTUP VALIDATOR — MARKET ANALYSIS AGENT")
print("=" * 60)

idea = input("\nEnter your startup idea: ")
industry = input("Enter the industry: ")
location = input("Enter the target location (e.g. India, USA, Global): ")

print("\nRunning agent — it will search and reason in multiple steps, this may take 20-40 seconds...\n")

result = run_market_analysis(idea, industry, location)

print("=" * 60)
print("MARKET ANALYSIS REPORT")
print("=" * 60)
print(f"\nLocation: {result.location}")
print(f"\nTAM: {result.tam}")
print(f"\nSAM: {result.sam}")
print(f"\nSOM: {result.som}")
print(f"\nGrowth Rate: {result.growth_rate}")
print(f"\nMarket Maturity: {result.market_maturity}")
print("\nCustomer Segments:")
for seg in result.customer_segments:
    print(f"  • {seg.name}: {seg.description}")
print("\nKey Trends:")
for trend in result.key_trends:
    print(f"  • {trend}")
print("\n" + "=" * 60)

# Also save the structured result to a JSON file for later use
import json
output_path = "last_analysis_result.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(result.model_dump(), f, indent=2, ensure_ascii=False)
print(f"\nStructured output also saved to: {output_path}")
