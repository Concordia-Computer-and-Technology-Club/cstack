"""
core/application.py
Ian Kollipara
2022.11.25

Cstack Main Application Configuration
"""

# Imports
from pathlib import Path
from tomllib import loads
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .api import API

PROJECT = loads(Path("pyproject.toml").read_text("utf-8"))


def Application(*, api: API, view_dist: str = "view/dist"):
    api = api
    view = StaticFiles(
        directory=f"{PROJECT['tool']['poetry']['name']}/{view_dist}", html=True
    )

    app = FastAPI()
    app.mount("/api", api.app, "api")
    app.mount("/", view, "frontend")
    return app
