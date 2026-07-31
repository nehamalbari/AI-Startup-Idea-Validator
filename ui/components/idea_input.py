import streamlit as st

def idea_input():

    col1, col2 = st.columns(2)

    with col1:

        startup = st.text_input(
            "💡 Startup Idea",
            placeholder="AI Resume Builder"
        )

        industry = st.selectbox(
            "Industry",
            [
                "AI",
                "Healthcare",
                "FinTech",
                "Education",
                "E-commerce"
            ]
        )

    with col2:

        location = st.selectbox(
            "Target Market",
            [
                "India",
                "USA",
                "Europe",
                "Global"
            ]
        )

        audience = st.selectbox(
            "Target Audience",
            [
                "Students",
                "Professionals",
                "Businesses",
                "Everyone"
            ]
        )

    analyze = st.button(
        "🚀 Analyze Startup",
        use_container_width=True
    )

    return startup, industry, location, audience, analyze