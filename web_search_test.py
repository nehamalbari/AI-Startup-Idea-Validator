from pipeline.graph import run_pipeline


startup_idea = """
AI fitness application for college students
with personalized workout and diet recommendations.
"""


result = run_pipeline(startup_idea)

print(result)