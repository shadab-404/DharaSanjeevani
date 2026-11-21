
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os

app = FastAPI(title="SmartAgri IoT Receiver")

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000/api/v1/sensors/data"
)


class SensorData(BaseModel):
    device_code: str = "ESP32_001"
    soil_moisture: float | None = None
    soil_temperature: float | None = None
    soil_ph: float | None = None
    nitrogen: float | None = None
    phosphorus: float | None = None
    potassium: float | None = None
    water_level: float | None = None
    water_flow: float | None = None
    proximity_cm: float | None = None


@app.get("/")
def home():
    return {
        "message": "SmartAgri IoT Receiver is running",
        "status": "online"
    }


@app.post("/sensor-data")
async def receive_sensor_data(data: SensorData):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                BACKEND_URL,
                json=data.model_dump(exclude_none=True)
            )

        response.raise_for_status()

        return {
            "message": "Sensor data forwarded successfully",
            "backend_status": response.status_code,
            "data": data.model_dump(exclude_none=True)
        }

    except httpx.HTTPError as error:
        raise HTTPException(
            status_code=502,
            detail=f"Backend forwarding failed: {str(error)}"
        )
