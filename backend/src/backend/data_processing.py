import pandas as pd
from backend.constants import DATA_DIRECTORY

df_lunar = pd.read_csv(DATA_DIRECTORY / "lunar.csv")
df_solar = pd.read_csv(DATA_DIRECTORY / "solar.csv")
