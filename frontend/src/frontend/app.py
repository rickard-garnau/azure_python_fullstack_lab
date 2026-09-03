import pandas as pd
import httpx
import os
import streamlit as st
from pathlib import Path
from views.lunar import lunar_metrics, plot_gamma_duration, LUNAR_TYPE_KEY
from views.solar import solar_metrics, plot_gamma_magnitude, SOLAR_TYPE_KEY
from views.eclipse_type import eclipse_types


BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

IMAGE_PATH = Path(__file__).parents[2] / "images"

st.markdown(
    "<h1 style='font-size: 3rem;'>Eclipsebord</h1>",
    unsafe_allow_html=True,
)

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
    st.error(f"Could not connect to backend for {dataset_name}-data.")
else:
    if dataset_name == "Lunar":
        st.subheader("Lunar Eclipse Analysis")
        st.image(IMAGE_PATH/"lunar_eclipse.jpg")
        lunar_metrics(df)
        plot_gamma_duration(df)
        eclipse_types(df, LUNAR_TYPE_KEY)
        st.subheader("Explore the data")
        st.dataframe(df)
    elif dataset_name == "Solar":
        st.subheader("Solar Eclipse Analysis")
        st.image(IMAGE_PATH/"solar_eclipse.jpg")
        solar_metrics(df)
        plot_gamma_magnitude(df)
        eclipse_types(df, SOLAR_TYPE_KEY)
        st.subheader("Explore the data")
        st.dataframe(df)
