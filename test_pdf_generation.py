from agents.pdf_generation_agent import run_pdf_generation_agent


test_report = {

    "startup_overview": {
        "idea_summary": "An AI-powered platform that helps college students find personalized internships.",
        "problem_statement": "College students struggle to discover internships that match their skills, interests, academic background, and career goals.",
        "target_users": [
            "College students",
            "Final-year students",
            "Recent graduates"
        ],
        "value_proposition": "Personalized AI-based internship recommendations based on individual student profiles."
    },

    "market_analysis": {
        "market_opportunity": "There is a significant opportunity in the growing AI-powered career and internship market.",
        "key_trends": [
            "Growth of AI-based career platforms",
            "Increasing demand for personalized job recommendations",
            "Growing adoption of digital internship platforms"
        ],
        "customer_demand": "Students increasingly seek personalized and relevant internship opportunities.",
        "key_insights": [
            "Personalization can improve internship discovery",
            "Students need better matching between skills and opportunities"
        ],
        "market_risks": [
            "Competition from established career platforms",
            "Difficulty obtaining accurate internship data"
        ]
    },

    "competitor_analysis": {
        "competitors": [
            "LinkedIn",
            "Internshala",
            "Indeed"
        ],
        "competitor_strengths": [
            "Large user base",
            "Large number of job and internship listings"
        ],
        "competitor_weaknesses": [
            "Limited personalization",
            "Generic search and recommendation experience"
        ],
        "competitive_advantages": [
            "AI-powered personalized matching",
            "Student-focused recommendations"
        ],
        "market_gaps": [
            "Lack of highly personalized internship recommendations for students"
        ]
    },

    "swot_analysis": {
        "strengths": [
            "Personalized AI recommendations",
            "Student-focused platform"
        ],
        "weaknesses": [
            "Requires quality student data",
            "Requires reliable internship listings"
        ],
        "opportunities": [
            "Partnerships with colleges",
            "Expansion into career guidance"
        ],
        "threats": [
            "Established competitors",
            "Changes in recruitment platforms"
        ]
    },

    "mvp_recommendation": {
        "development_focus": "Build a basic AI-powered internship matching platform focused on student profiles and personalized recommendations.",
        "core_features": [
            "Student profile creation",
            "AI internship matching",
            "Internship search",
            "Personalized recommendations"
        ],
        "features_to_delay": [
            "Advanced career coaching",
            "Employer analytics"
        ],
        "implementation_considerations": [
            "Build a reliable student profile system",
            "Develop the recommendation engine",
            "Integrate reliable internship data sources"
        ]
    },

    "go_to_market": {
        "positioning": "An AI-powered personalized internship discovery platform designed specifically for college students.",
        "customer_segments": [
            "College students",
            "Final-year students",
            "Recent graduates"
        ],
        "acquisition_channels": [
            "College partnerships",
            "Student communities",
            "Social media"
        ],
        "launch_strategy": [
            "Launch at selected colleges",
            "Run student-focused campaigns",
            "Collect feedback and improve recommendations"
        ],
        "pricing_strategy": "Offer the student-facing platform for free initially and explore premium career services later."
    },

    "final_recommendation": {
        "startup_viability": "The startup has good potential if it can provide accurate personalized recommendations and maintain a reliable internship database.",
        "overall_score": 8,
        "key_reasons": [
            "Clear student problem",
            "Growing demand for personalized career services",
            "Potential for AI differentiation"
        ],
        "major_risks": [
            "Competition from established platforms",
            "Data quality",
            "User acquisition"
        ],
        "next_steps": [
            "Develop the MVP",
            "Partner with colleges",
            "Test the recommendation system with students"
        ]
    }
}


result = run_pdf_generation_agent(test_report)

print("PDF Agent Result:")
print(result)