import os
import httpx
import streamlit as st
import pandas as pd

BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.title("eClipseBord")

tab1, tab2 = st.tabs(["Lunar Eclipse", "Solar Eclipse"])

with tab1:
    st.subheader("Lunar Eclipse")
    st.image("assets/lunar_eclipse.jpg")
    st.caption("A lunar eclipse happens when Earth passes directly between the Sun and the Moon, blocking sunlight and casting a shadow on the lunar surface.")
    try:
        response = httpx.get(f"{BASE_URL}/lunar/data")
        response.raise_for_status()
        df_lunar = pd.DataFrame(response.json())
        st.metric("Total rows of lunar eclipses", len(df_lunar))
        st.scatter_chart(df_lunar[["Gamma", "Penumbral Magnitude"]])
        st.dataframe(df_lunar)
        
    except httpx.RequestError:
        st.error("Could not connect to lunar data")

with tab2:
    st.subheader("Solar Eclipse")
    st.image("assets/solar_eclipse.jpg")
    st.caption("When the Moon passes directly between the Sun and Earth, it blocks the Sun's light and casts a shadow on Earth, causing a solar eclipse.")
    try:
        response = httpx.get(f"{BASE_URL}/solar/data")
        response.raise_for_status()
        df_solar = pd.DataFrame(response.json())
        st.metric("Total rows of solar eclipses", len(df_solar))
        st.scatter_chart(df_solar[["Gamma", "Eclipse Magnitude"]])
        st.dataframe(df_solar)
    except httpx.RequestError:
        st.error("Could not connect to solar data")