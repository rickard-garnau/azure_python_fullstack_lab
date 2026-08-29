from fastapi import FastAPI
from backend.data_processing import df_solar, df_lunar

app = FastAPI()

@app.get("/lunar/data")
async def get_lunar_data():
    return df_lunar.to_dict(orient="records")

@app.get("/solar/data")
async def get_solar_data():
    return df_lunar.to_dict(orient="records")