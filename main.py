from contextlib import asynccontextmanager
from functools import lru_cache

from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: str
    app_name: str = "Sound Money Projection (Online!)"
    model_config = SettingsConfigDict(env_file=".env", extra="allow")


@lru_cache()
def get_settings():
    return Settings()


app = FastAPI(generate_unique_id_function=lambda x: f"{x.name}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def index(repoonse_class=HTMLResponse):
    return HTMLResponse(
        content="<html><body><h1>Sound Money Projection (Online!)</h1></body></html>",
        status_code=200,
    )


@app.get("/v1/api/projection/myoutlook")
async def get_projection_by_age(age: int, response_class=HTMLResponse):
    return HTMLResponse(
        content="<html><body><h1>Sound Money Projection (Online!)</h1></body><div>You'll never have enough money left to consume what your litle heart desires.</div></html>",
        status_code=200,
    )


@app.get("/v1/api/projection/myspending")
async def get_projection_by_spending(
    age: int, daily_spending: int, response_class=HTMLResponse
):
    return HTMLResponse(
        content="<html><body><h1>Sound Money Projection (Online!)</h1></body><div>You're XX % through your life and at a rate of $XX per day, you'll need $XXX,XXX,XXX to live.</div></html>",
        status_code=200,
    )


@app.get("/v1/api/projection/lifetime")
async def get_projection_by_spending(
    age: int,
    daily_spending: int,
    current_savings: int,
    num_children: int = 0,
    response_class=HTMLResponse,
):
    return HTMLResponse(
        content="<html><body><h1>Sound Money Projection (Online!)</h1></body><div>You're XX % through your life and at a rate of $XX per day, you'll need $XXX,XXX,XXX to live.</div></html>",
        status_code=200,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
