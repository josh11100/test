from __future__ import annotations
from typing import Optional, List, Dict
import re
import pandas as pd
import streamlit as st
from urllib.parse import quote_plus

from utils.fetch import fetch
from utils.parsing import parse_ivproperties_listings

def _price_to_int(p: str) -> Optional[int]:
    m = re.search(r"(\$?)([\d,]+)", p or "")
    if not m:
        return None
    try:
        return int(m.group(2).replace(",", ""))
    except Exception:
        return None

def housing_page():
    st.header("🏠 Isla Vista Housing (beta)")
    st.caption("Data pulled live from public pages when possible. Always verify details with the property manager.")

    col_a, col_b, col_c, col_d, col_e = st.columns([2,1,1,1,1])
    with col_a:
        q = st.text_input("Search keyword (optional)", placeholder="2 bed, Del Playa, studio…")
    with col_b:
        max_price = st.number_input("Max $/mo (optional)", min_value=0, value=0, step=50)
    with col_c:
        beds = st.selectbox("Bedrooms", ["Any", "Studio", "1", "2", "3", "4+"], index=0)
    with col_d:
        sublease = st.checkbox("Sublease")
    with col_e:
        fetch_btn = st.button("Fetch IVProperties")

    st.markdown(
        """
        <div class='small muted'>
        <span class='pill'>Source</span> ivproperties.com · Respect robots.txt · Use responsibly
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not fetch_btn:
        return

    with st.spinner("Contacting ivproperties.com…"):
        url = f"https://www.ivproperties.com/?q={quote_plus(q)}" if q else "https://www.ivproperties.com/"
        resp = fetch(url)
        if not resp:
            st.warning("Could not reach ivproperties.com (or blocked). Try again later.")
            return

        listings = parse_ivproperties_listings(resp.text)
        rows: List[Dict] = []
        for L in listings:
            p_int = _price_to_int(L.price)
            if max_price and (p_int is not None) and p_int > max_price:
                continue
            if beds != "Any":
                if beds == "4+":
                    b = re.search(r"(\d+)", L.beds or "")
                    if not (b and int(b.group(1)) >= 4):
                        continue
                else:
                    if beds.lower() not in (L.beds or "").lower():
                        continue

            link = L.link if L.link.startswith("http") else (f"https://www.ivproperties.com{L.link}" if L.link else "")
            rows.append(
                {"Title": L.title, "Address": L.address, "Price": L.price, "Beds": L.beds, "Baths": L.baths, "Link": link}
            )

        # keyword and sublease filters
        if q:
            ql = q.lower()
            rows = [r for r in rows if any(ql in str(v).lower() for v in (r["Title"], r["Address"], r["Beds"], r["Baths"]))]
        if sublease:
            rows = [r for r in rows if "sublease" in r["Title"].lower() or "sublease" in r["Address"].lower()]

        if not rows:
            st.info("No matching results (or the site's markup changed). Try clearing filters.")
            return

        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True)
        for r in rows:
            st.markdown(f"- [{r['Title']}]({r['Link']}) — {r['Price']} · {r['Beds']} · {r['Baths']} · {r['Address']}")
        st.success("Fetched listings. Always cross-check availability with the property manager.")

    with st.expander("⚖️ Legal & ethics (read me)"):
        st.write(
            """
            • Scraping public pages can break if the site changes. Keep requests minimal and cached.
            • Check each site's Terms of Service and robots.txt. If scraping is disallowed, remove it.
            • Prefer official APIs or email the property manager for a feed.
            """
        )
