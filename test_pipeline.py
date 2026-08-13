from pipeline.graph import run_pipeline


startup_idea = """
An AI-powered platform that helps college students find personalized
internships based on their skills, interests, academic background,
and career goals.
"""


result = run_pipeline(startup_idea)

print("\n========== PDF OUTPUT ==========")
print(result["pdf"])

print("\n========== REPORT GENERATED ==========")
print("Yes")
