from pdf_generator.generate_pdf import generate_pdf


sample_report = {

    "startup_overview": {

        "idea_summary": "AI powered fitness assistant",

        "problem_statement":
        "Users struggle with personalized workout planning"

    },


    "swot_summary": {

        "strengths": [
            "AI recommendations",
            "Personalization"
        ],

        "weaknesses": [
            "Needs user data"
        ],

        "opportunities": [
            "Growing health technology market"
        ],

        "threats": [
            "Competition from fitness apps"
        ]

    }

}


pdf = generate_pdf(sample_report)


print(
    "Generated:",
    pdf
)