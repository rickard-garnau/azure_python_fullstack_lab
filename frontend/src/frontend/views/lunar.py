import pandas as pd
import streamlit as st


def lunar_metrics(df: pd.DataFrame):
    avg_gamma = round(df["Gamma"].mean(), 2)
    max_duration = df["Total Eclipse Duration (m)"].max()

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Average Gamma", value=avg_gamma)
    with col2:
        st.metric(label="Max duration", value=f"{max_duration} min")

def plot_gamma_duration(df: pd.DataFrame) -> None:
    st.write("Conjuction between Gamma and Duration")
    st.scatter_chart(
        data=df,
        x="Gamma",
        y="Total Eclipse Duration (m)",
    )