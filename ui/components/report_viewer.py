import streamlit as st

def report_viewer(web_result, market_result):

    tabs = st.tabs([
        "🌐 Web Search",
        "📈 Market Analysis",
        "⚔ SWOT",
        "📢 GTM",
        "📦 MVP",
        "📄 Final Report"
    ])

    with tabs[0]:

        st.subheader("🌐 Web Search")

        st.markdown(web_result)

    with tabs[1]:

        st.subheader("📈 Market Analysis")

        st.write(market_result)

    with tabs[2]:

        st.info("Waiting for SWOT Agent")

    with tabs[3]:

        st.info("Waiting for GTM Agent")

    with tabs[4]:

        st.info("Waiting for MVP Agent")

    with tabs[5]:

        st.info("Waiting for Final Report Agent")