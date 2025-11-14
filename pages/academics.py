from __future__ import annotations
import pandas as pd
import streamlit as st

MAJOR_SHEETS = {
    "Statistics & Data Science": "https://www.pstat.ucsb.edu/undergrad/majors",
    "Computer Science": "https://www.cs.ucsb.edu/education/undergraduate",
    "Economics": "https://econ.ucsb.edu/undergrad",
    "Mathematics": "https://www.math.ucsb.edu/undergrad",
}

def academics_page():
    st.header("🎓 Academics — advising quick links")
    st.caption("Every major has its own plan sheet / prereqs. These are placeholders — swap with official UCSB links.")

    col1, col2 = st.columns([1.2, 2])
    with col1:
        major = st.selectbox("Pick a major", list(MAJOR_SHEETS.keys()))
        st.link_button("Open major planning page", MAJOR_SHEETS[major])
        st.divider()
        st.subheader("General tips")
        st.markdown(
            """
            - Check for **pre-major** vs **full major** requirements early.
            - Balance load: 1–2 heavy technicals + 1 lighter GE when possible.
            - Use GOLD waitlist smartly; watch enrollment windows.
            - Talk to advisors and upperclassmen in your dept Discord/Slack.
            """
        )
    with col2:
        st.subheader("Build your quarter (scratchpad)")
        data = st.experimental_data_editor(
            pd.DataFrame(
                [
                    {"Course": "PSTAT 120A", "Units": 4, "Type": "Major"},
                    {"Course": "MATH 6A", "Units": 4, "Type": "Support"},
                    {"Course": "GE Area D", "Units": 4, "Type": "GE"},
                ]
            ),
            use_container_width=True,
            num_rows="dynamic",
        )
        st.metric("Planned units", int(sum(data["Units"])) if not data.empty else 0)

    with st.expander("🔗 Add more official links"):
        st.write("Paste your department URLs here for quick access in future iterations.")
