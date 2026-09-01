import streamlit as st
import pandas as pd
from views.gamma import render_gamma_metric

""" LLM solution:
type_key is passed in rather than hardcoded because lunar and solar have different eclipse type codes, so the explanation text can't be shared
"""

LUNAR_TYPE_KEY = [ 
    "N — Penumbral eclipse (Moon passes only through Earth's penumbra, not the umbra)",
    "P — Partial eclipse (part of the Moon in Earth's umbra)",
    "T — Total eclipse (whole Moon in Earth's umbra)",
    "A letter followed by b/e means first/last in its Saros series; x means a total penumbral eclipse; + / − means the total eclipse's center passes north or south of the shadow axis.",
]


def lunar_metrics(df: pd.DataFrame):
    max_duration = df["Total Eclipse Duration (m)"].max()
    col1, col2 = st.columns(2)
    render_gamma_metric(df, col1)
    with col2:
        st.metric(label="Max duration", value=f"{max_duration} min")

def plot_gamma_duration(df: pd.DataFrame) -> None:
    st.write("Conjunction between Gamma and Duration to define how long an eclipse will last. A low Gamma means the Moon passes centrally through Earth's shadow, giving a long duration. A high Gamma means a more off-center pass, giving a short duration.")
    st.scatter_chart(
        data=df,
        x="Gamma",
        y="Total Eclipse Duration (m)",
        color="#BDC3CC",
    )