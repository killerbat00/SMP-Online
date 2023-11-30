from contextlib import asynccontextmanager
from functools import lru_cache

from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: str
    app_name: str = "Realistic Financial Outlook"
    model_config = SettingsConfigDict(env_file=".env", extra="allow")


@lru_cache()
def get_settings():
    return Settings()


app = FastAPI(generate_unique_id_function=lambda x: f"{x.name}")

app.mount("/static", app=StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/v1/api/outlook")
async def get_outlook(age: int, response_class=HTMLResponse):
    return HTMLResponse(
        content="<html><body><h1>Realistic Financial Outlook</h1></body><div>You'll never have enough money left to consume what your litle heart desires.</div></html>",
        status_code=200,
    )


@app.get("/v1/api/spending")
async def get_projection_by_spending(
    age: int, daily_spending: int, response_class=HTMLResponse
):
    return HTMLResponse(
        content="<html><body><h1>Realistic Financial Outlook</h1></body><div>You're XX % through your life and at a rate of $XX per day, you'll need $XXX,XXX,XXX to live.</div></html>",
        status_code=200,
    )
