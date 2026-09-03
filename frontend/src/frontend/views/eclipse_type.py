import streamlit as st
import pandas as pd

# A function that both lunar and solar can use
def eclipse_types(df: pd.DataFrame, type_key) -> None:
    st.write("Different types of eclipses")
    st.bar_chart(
        df["Eclipse Type"].value_counts(),
        x_label = "Different eclipses",
        y_label = "Amount",
        color="#FFFFFF",
        width="stretch",
        height="content",
        horizontal=True
        )
    with st.expander("What does each type mean?"):
        for line in type_key:
            st.write(line)