import os
import httpx
import streamlit as st

BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

tab1, tab2 = st.tabs(["Lunar Eclipse", "Solar Eclipse"], on_change="rerun")

with tab1:
    st.header("Lunar Eclipse")
    if tab1.open:
        lunar_data = httpx.get(f"{BASE_URL}/lunar/data").json()
        st.dataframe(lunar_data)

with tab2:
    st.header("Solar Eclipse")
    if tab2.open:
        solar_data = httpx.get(f"{BASE_URL}/solar/data").json()
        st.dataframe(solar_data)