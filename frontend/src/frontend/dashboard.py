import os
import httpx
import streamlit as st

BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

def main():
    st.markdown("# Lunar Eclipse")
    st.write(BASE_URL)
    data = httpx.get(f"{BASE_URL}/lunar/data", timeout=30).json()
    st.dataframe(data)

if __name__ == "__main__":
    main()