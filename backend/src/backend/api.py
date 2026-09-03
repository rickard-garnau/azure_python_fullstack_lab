from fastapi import FastAPI
from backend.data_processing import df_solar, df_lunar
import json

app = FastAPI()

@app.get("/lunar/data")
async def get_lunar_data():
    return json.loads(df_lunar.to_json(orient="records")) # "to_json" instead of "to_dict" to automatically convert NaN to Null to avoid ValueError

@app.get("/solar/data")
async def get_solar_data():
    return json.loads(df_solar.to_json(orient="records"))