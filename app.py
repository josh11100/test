from __future__ import annotations
from pathlib import Path
from typing import Dict, Any
import streamlit as st

# Import page modules
from pages.housing import housing_page
from pages.academics import academics_page
from pages.locator import locator_page
from pages.professors import profs_page
from pages.aid_jobs import aid_jobs_page
from pages.qa import qa_page

st.set_page_config(page_title="gauchoGPT — UCSB helper", page_icon="🧢", layout="wide")

# Load external CSS
css_path = Path("assets/styles.css")
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

st.sidebar.title("🧢 gauchoGPT")
st.sidebar.caption("UCSB helpers — housing • classes • professors • aid • jobs")

PAGES: Dict[str, Any] = {
    "Housing (IV)": housing_page,
    "Academics": academics_page,
    "Class Locator": locator_page,
    "Professors": profs_page,
    "Aid & Jobs": aid_jobs_page,
    "Q&A (WIP)": qa_page,
}

choice = st.sidebar.radio("Navigate", list(PAGES.keys()))
PAGES[choice]()

st.sidebar.divider()
st.sidebar.markdown(
    """
**Next steps**
- Swap placeholder links with official UCSB URLs you trust.
- Expand the ivproperties parser for site-specific selectors.
- Add caching and rate limiting if you fetch often.
- Connect an LLM for the Q&A tab.
"""
)
