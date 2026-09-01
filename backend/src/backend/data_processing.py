import pandas as pd
from backend.constants import DATA_DIRECTORY

df_lunar = pd.read_csv(DATA_DIRECTORY / "lunar.csv")

df_lunar["Total Eclipse Duration (m)"] = pd.to_numeric(
    df_lunar["Total Eclipse Duration (m)"], errors="coerce"
)

df_solar = pd.read_csv(DATA_DIRECTORY / "solar.csv")
