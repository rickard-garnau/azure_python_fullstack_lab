import pandas as pd
import streamlit as st
from views.gamma import render_gamma_metric

""" LLM solution:
type_key is passed in rather than hardcoded because lunar and solar have different eclipse type codes, so the explanation text can't be shared
"""

SOLAR_TYPE_KEY = [ 
    "P — Partial eclipse (Moon covers part of the Sun)",
    "A — Annular eclipse (Moon covers the Sun's center, leaving a ring of light)",
    "T — Total eclipse (Moon fully covers the Sun)",
    "H — Hybrid eclipse (total along part of its path, annular along the rest)",
    "A letter followed by b/m/e means first/middle/last in its Saros series; + / − means the path runs north or south of center.",
]

def solar_metrics(df: pd.DataFrame):
    max_magnitude = df["Eclipse Magnitude"].max()
    col1, col2 = st.columns(2)
    render_gamma_metric(df, col1)
    with col2:
        st.metric(label="Max Magnitude", value=max_magnitude)

def plot_gamma_magnitude(df: pd.DataFrame) -> None:
    st.write("Conjunction between Gamma and Magnitude to define how an eclipse will look. A low Gamma means the Moon passes centrally in front of the Sun, giving a high magnitude closer to total coverage. A high Gamma means a more off-center pass, giving a low magnitude only a partial eclipse.")
    st.scatter_chart(
        data=df,
        x="Gamma",
        y="Eclipse Magnitude",
        color="#E3FF21",
    )  

