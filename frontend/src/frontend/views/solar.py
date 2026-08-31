import pandas as pd
import streamlit as st

def solar_metrics(df: pd.DataFrame):
    avg_gamma = round(df["Gamma"].mean(), 2)
    max_magnitude = df["Eclipse Magnitude"].max()

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Average Gamma", value=avg_gamma)
    with col2:
        st.metric(label="Max Magnitude", value=max_magnitude)

def plot_gamma_magnitude(df: pd.DataFrame) -> None:
    st.write("Conjuction between Gamma and Magnitude")
    st.scatter_chart(
        data=df,
        x="Gamma",
        y="Eclipse Magnitude"
    )