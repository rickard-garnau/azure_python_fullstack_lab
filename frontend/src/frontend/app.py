import pandas as pd
import httpx
import os
import streamlit as st
from views.lunar import lunar_metrics, plot_gamma_duration
from views.solar import solar_metrics, plot_gamma_magnitude

BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.title("eClipseBord")
st.write("Explore eclipses")

dataset_name = st.sidebar.selectbox("Select dataset", ("Lunar", "Solar"))

def get_dataset(name: str) -> pd.DataFrame | None:
    endpoint = "/lunar/data" if name == "Lunar" else "/solar/data"
    try:
        response = httpx.get(f"{BASE_URL}{endpoint}", timeout=30)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except (httpx.RequestError, httpx.HTTPStatusError):
        return None

df = get_dataset(dataset_name)

if df is None:
    st.error(f"Kunde inte ansluta till backend för {dataset_name}-data.")
else:
    if dataset_name == "Lunar":
        st.subheader("Lunar Eclipse Analysis")
        lunar_metrics(df)
        plot_gamma_duration(df)
        st.dataframe(df)
    elif dataset_name == "Solar":
        st.subheader("Solar Eclipse Analysis")
        solar_metrics(df)
        plot_gamma_magnitude(df)
        st.dataframe(df)
