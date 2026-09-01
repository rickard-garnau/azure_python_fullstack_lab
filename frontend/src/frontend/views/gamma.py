import pandas as pd
import streamlit as st

# The avg-gamma logic that was identical in lunar/solar, (Which LLM made me aware of) changed to a callable function to keep it DRY. 
def render_gamma_metric(df: pd.DataFrame, column) -> None:
    avg_gamma = round(df["Gamma"].mean(), 2)
    with column:
        st.metric(label="Average Gamma", value=avg_gamma)