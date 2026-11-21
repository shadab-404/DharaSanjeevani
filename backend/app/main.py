
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.connection import engine
from app.database.base import Base
from app import models

from app.routes import sensors
from app.routes import crops
from app.routes import irrigation
from app.routes import alerts


app = FastAPI(
    title=settings.APP_NAME,
    description="Smart Agriculture Monitoring and Irrigation API",
    version="1.0.0"
)


# CORS Configuration - Only one middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create database tables
@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


# Register API routes
app.include_router(
    sensors.router,
    prefix=settings.API_V1_PREFIX
)

app.include_router(
    crops.router,
    prefix=settings.API_V1_PREFIX
)

app.include_router(
    irrigation.router,
    prefix=settings.API_V1_PREFIX
)

app.include_router(
    alerts.router,
    prefix=settings.API_V1_PREFIX
)


@app.get("/")
def home():
    return {
        "message": "Welcome to SmartAgri API",
        "status": "running"
    }


@app.get(f"{settings.API_V1_PREFIX}/health")
def health_check():
    return {
        "status": "healthy",
        "project": "SmartAgri"
    }

