from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from app.database import engine
from app.routers import heros, mission, teams


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)   # create missing tables
    yield


app = FastAPI(
    title="Heroes API",
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "heroes", "description": "Create, read, update and delete heroes."},
        {"name": "teams", "description": "Teams and the heroes that belong to them."},
        {"name": "missions", "description": "Missions assigned to heroes."},
    ],
)

app.include_router(heros.router, prefix="/api/v1")
app.include_router(teams.router, prefix="/api/v1")
app.include_router(mission.router, prefix="/api/v1")

cors_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5500,http://127.0.0.1:5500",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
