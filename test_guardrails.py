from guardrails.input_guardrail import validate_startup_idea
from guardrails.output_guardrail import validate_pipeline_output


print("INPUT GUARDRAIL TESTS")
print("--------------------")

# Valid input
result = validate_startup_idea(
    "An AI platform that helps small businesses analyze customer feedback."
)
print("Valid input:", result)

# Empty input
result = validate_startup_idea("")
print("Empty input:", result)

# Invalid test input
result = validate_startup_idea("hello")
print("Invalid input:", result)

# Too short
result = validate_startup_idea("AI")
print("Short input:", result)


print("\nOUTPUT GUARDRAIL TESTS")
print("---------------------")

# Valid output
valid_output = {
    "report": {
        "startup_overview": "AI startup validation report"
    },
    "pdf": "report.pdf"
}

result = validate_pipeline_output(valid_output)
print("Valid output:", result)

# Empty output
result = validate_pipeline_output({})
print("Empty output:", result)

# Missing report
result = validate_pipeline_output({
    "pdf": "report.pdf"
})
print("Missing report:", result)

# Missing PDF
result = validate_pipeline_output({
    "report": {
        "startup_overview": "AI startup validation report"
    }
})
print("Missing PDF:", result)